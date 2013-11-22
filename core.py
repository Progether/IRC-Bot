import socket, re

from settings import read_config

class IRCBot:
    
    logAllToConsole = False                 # dev boolean to toggle raw printing of all messages to console
    respondToUnrecognisedCommands = False   # respond to user if they enter a command that isn't registered
    
    def __init__(self, tempCacheSize=4096):
        ### configuration
        conf = read_config()
        self.nickname    = conf['nick']
        self.password    = conf['password']
        self.channel     = '#%s' % conf['channel']
        self.network     = conf['network']
        self.port        = int(conf['port'])
        
        self.command_prefix    = conf['command_prefix']
        self.quitCmd           = conf['quit']
        self.logAllToConsole   = conf['logAllToConsole'] == 'True'
        self.respondToNotFound = conf['respondToNotFound'] == 'True'
        
        ### connection
        self.socket        = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tempCacheSize = tempCacheSize

        ### addons
        self.addonList = list()
        
        ### tests for messages received from server
        self.regexIsError             = re.compile(r"^ERROR*")
        self.regexIsJoin              = re.compile(r":(?P<user>\w+)!.+\sJOIN\s")
        self.regexIsQuit              = re.compile(r":(?P<user>\w+)!.+\sPART\s")
        self.regexIsCommand           = re.compile(r"^%s{1}(?P<command>\w+)" % self.command_prefix)
        self.regexCommandSplitCommand = re.compile(r"^%s{1}(?P<command>\w+)\s(?P<arguments>.*).*" % self.command_prefix)
        self.regexIsChat              = re.compile(r":(?P<user>\w+)!(?P<isp>.+)\sPRIVMSG\s(?P<channel>[#\w-]+)\s:(?P<message>.+)")
        self.regexIsNickInUse         = re.compile(r".*\s433\s.?%s.*" % self.nickname)
        self.regexIsAskForLogin       = re.compile(r".*ʌ")
        # '...freenode.net 461 indibot JOIN :Not enough parameters\r\n'
        

    def run(self):
        self.socket.connect((self.network, self.port))
        self.log(self.socket.recv(self.tempCacheSize).decode("UTF-8"))
        string = 'NICK %s \r\n' % self.nickname
        self.socket.send(string.encode("UTF-8"))
        string = 'USER %s some stuff :Python IRC\r\n' % self.nickname
        self.socket.send(string.encode("UTF-8"))
        string = 'JOIN %s \r\n' % self.channel
        self.socket.send(string.encode("UTF-8"))
        
        self.mainLoop()

    def mainLoop(self):
        while True:
            receivedData = self.socket.recv(self.tempCacheSize).decode("UTF-8")
            messageInfo = dict()
            
            if (self.logAllToConsole):
                print("-- %s" % receivedData.encode('utf-8'))
            
            isError     = self.regexIsError.match(receivedData)
            if isError:
                self.log("!! CAUGHT ERROR ::> " +receivedData)
                self.log("!! Quitting")
                return 1
            
            isNickInUse = self.regexIsNickInUse.match(receivedData)
            if isNickInUse:
                import ircHelpers    # dirty hack - should be moved somewhere more applicable (ie at !!nick)
                ircHelpers.sayInChannel("Nick is already in use")
            
            isChat = self.regexIsChat.match(receivedData)
            if isChat:
                # parse message
                messageInfo['user']    = isChat.group('user')
                messageInfo['isp']     = isChat.group('isp')
                messageInfo['channel'] = isChat.group('channel')
                messageInfo['message'] = isChat.group('message')

                # if it is a command, find addon and execute command
                isCommand = self.regexIsCommand.match(messageInfo['message'])
                if isCommand:
                    split = self.regexCommandSplitCommand.match(messageInfo['message'])
                    commandName = split.group('command')
                    commandArguments = split.group('arguments')
                    isAddon = False
                    for addon in self.addonList:
                        if commandName in addon.commandList:
                            addon.commandList[commandName](commandArguments, messageInfo)
                            isAddon = True
                    if not isAddon and self.respondToNotFound:
                        string = "NOTICE %s :I don't know that command\r\n" % (messageInfo['user'])
                        self.socket.send(string.encode('UTF-8'))
                
                elif messageInfo['channel'] == self.channel:
                    for addon in self.addonList:
                        for messageMethod in addon.messageList:
                            messageMethod(messageInfo)
                          
            # if new join, greet
            isJoin = self.regexIsJoin.match(receivedData)
            if isJoin:
                for addon in self.addonList:
                    for joinMethod in addon.joinList:
                        joinMethod(isJoin.group('user'))

            # if user leaves channel, update their database info
            isQuit = self.regexIsQuit.match(receivedData)
            if isQuit:
                for addon in self.addonList:
                    for quitMethod in addon.quitList:
                        quitMethod(isQuit.group('user'))
            
            #make sure we don't time out of server
            if receivedData.find('PING') != -1:
                string = 'PONG %s \r\n' % receivedData.split()[1]
                self.socket.send(string.encode("UTF-8"))
            else:
                # moved log here to filter out ping/pong chatter
                self.log(receivedData.encode('utf-8'))

    def log(self, stringToLog):
        #change eventually to log in a file but for now print is fine
        print(">> %s" % stringToLog)

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
    quitList = list()

ircBot = IRCBot()

