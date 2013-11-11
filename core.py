import socket, re

from settings import read_config

class IRCBot:
    def __init__(self, tempCacheSize=4096):
        conf = read_config()
        self.network = conf['network']
        self.port = int(conf['port'])
        self.channel = conf['channel']
        self.quitCmd = conf['quit']
        self.nickname = conf['nick']
        self.password = conf['password']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bot_command = conf['bot_command']
        
        self.tempCacheSize = tempCacheSize

        self.addonList = list()

        self.regexIsJoin = re.compile(r":(?P<user>\w+)!.+\sJOIN\s")
        self.regexIsCommand = re.compile(r"(?P<command>%s..+)" % self.bot_command)
        self.regexCommandSplitCommand = re.compile(r"%s(?P<command>\w+)\s(?P<arguments>.*).*" % self.bot_command)
        self.regexIsChat = re.compile(r":(?P<user>\w+)!(?P<isp>.+)\sPRIVMSG\s(?P<channel>[#\w-]+)\s:(?P<message>.+)")

    def run(self):
        self.socket.connect((self.network, self.port))
        self.log(self.socket.recv(self.tempCacheSize).decode("UTF-8"))
        string = 'NICK %s \r\n' % self.nickname
        self.socket.send(string.encode("UTF-8"))
        string = 'USER %s some stuff :Python IRC\r\n' % self.nickname
        self.socket.send(string.encode("UTF-8"))
        string = 'JOIN %s \r\n' % self.channel
        self.socket.send(string.encode("UTF-8"))
        
        # need to register bot nick bofre you can use this. If you'd rather skip register comment out next lines.
        #self.socket.send('PRIVMSG NickServ :IDENTIFY %s %s\r\n' % (self.nickname, self.password))
        
        self.mainLoop()

    def mainLoop(self):
        while True:
            receivedData = self.socket.recv(self.tempCacheSize).decode("UTF-8")
            #self.log(recievedData)
            messageInfo = dict()
            isChat = self.regexIsChat.match(receivedData)
            if isChat:
                messageInfo['user'] = isChat.group('user')
                messageInfo['isp'] = isChat.group('isp')
                messageInfo['channel'] = isChat.group('channel')
                messageInfo['message'] = isChat.group('message')

                isCommand = self.regexIsCommand.match(messageInfo['message'])
                if isCommand:
                    split = self.regexCommandSplitCommand.match(messageInfo['message'])
                    commandName = split.group('command')
                    commandArguments = split.group('arguments')
                    for addon in self.addonList:
                      if commandName in addon.commandList:
                        addon.commandList[commandName](commandArguments, messageInfo)
                elif messageInfo['channel'] == self.channel:
                    for addon in self.addonList:
                        for messageMethod in addon.messageList:
                            messageMethod(messageInfo)

            isJoin = self.regexIsJoin.match(receivedData)
            if isJoin:
                for addon in self.addonList:
                    for joinMethod in addon.joinList:
                        joinMethod(isJoin.group('user'))

            for addon in self.addonList:
                for behaviour in addon.behaviourList:
                    behaviour(receivedData)
            
            #temporary quit method, should be changed so only admins can use
            if receivedData.find(self.quitCmd) != -1:
                self.log("Quitting")
                string = 'QUIT\r\n'
                self.socket.send(string.encode("UTF-8"))
                break
            
            #make sure we don't time out of server
            if receivedData.find('PING') != -1:
                string = 'PONG %s \r\n' % receivedData.split()[1]
                self.socket.send(string.encode("UTF-8"))
            else:
                # moved log here to filter out ping/pong chatter
                self.log(receivedData)

    def log(self, stringToLog):
        #change eventually to log in a file but for now print is fine
        print(stringToLog)

    def registerAddon(self, **options):
        def decorator(f):
            self.addonList.append(f())
            return f
        return decorator

class AddonBase:
    commandList = dict()
    behaviourList = list()
    messageList = list()
    joinList = list()

ircBot = IRCBot()

