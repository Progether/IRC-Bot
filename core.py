import socket
import re
import yaml
import os.path


class IRCBot:

    logAllToConsole = False                 # dev boolean to toggle raw printing of all messages to console
    respondToUnrecognisedCommands = False   # respond to user if they enter a command that isn't registered

    def __init__(self, conf, temp_cache_size=4096):
        """
        Creates a new IRCBot object.

        :param conf: the configuration dictionary to use to connect, etc.
        :type conf: dict
        """
        # If no configuration provided, error out with a ConfError
        if conf == {}:
            raise ConfigurationError("No configuration provided")

        # Otherwise, store the useful config info
        self.nickname = conf['user']['nick']
        self.password = conf['user']['password']
        self.channel = '#%s' % conf['channel']['name']
        self.network = conf['channel']['network']
        self.port = conf['channel']['port']

        self.command_prefix = conf['settings']['prefix']
        self.logAllToConsole = conf['settings']['logAllToConsole']
        self.respondToNotFound = conf['settings']['respondToNotFound']

        ### connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.temp_cache_size = temp_cache_size

        ### addons
        self.addonList = list()

        ### tests for messages received from server
        self.regexIsError = re.compile(r"^ERROR.*|\\r\\nError.*")
        self.regexIsJoin = re.compile(r":(?P<user>\w+)!.+\sJOIN\s")
        self.regexIsQuit = re.compile(r":(?P<user>\w+)!.+\sPART\s")
        self.regexIsCommand = re.compile(r"^%s{1}(?P<command>\w+)" % self.command_prefix)
        self.regexCommandSplitCommand = re.compile(r"^%s{1}(?P<command>\w+)\s(?P<arguments>.*).*" % self.command_prefix)
        self.regexIsChat = re.compile(r":(?P<user>\w+)!(?P<isp>.+)\sPRIVMSG\s(?P<channel>[#\w-]+)\s:(?P<message>.+)")
        self.regexIsNickInUse = re.compile(r".*\s433\s.?%s.*" % self.nickname)
        self.regexIsAskForLogin = re.compile(r".*ʌ")
        # '...freenode.net 461 indibot JOIN :Not enough parameters\r\n'

    def run(self):
        self.socket.connect((self.network, self.port))
        self.logInfo(self.socket.recv(self.temp_cache_size).decode("UTF-8"))
        string = 'NICK %s \r\n' % self.nickname
        self.socket.send(string.encode("UTF-8"))
        string = 'USER %s some stuff :Python IRC\r\n' % self.nickname
        self.socket.send(string.encode("UTF-8"))
        string = 'JOIN %s \r\n' % self.channel
        self.socket.send(string.encode("UTF-8"))

        self.main_loop()

    def main_loop(self):
        import ircHelpers    # dirty hack - should be moved somewhere more applicable (ie at !!nick)
        ircHelpers.start_queue_thread()
        while True:
            receivedData = self.socket.recv(self.temp_cache_size).decode("UTF-8")
            messageInfo = dict()

            if (self.logAllToConsole):
                print("-- %s" % receivedData.encode('utf-8'))

            isError     = self.regexIsError.match(receivedData)
            if isError:
                self.logError("CAUGHT ERROR ::> " +receivedData)
                self.logError("Quitting")
                return 1

            isNickInUse = self.regexIsNickInUse.match(receivedData)
            if isNickInUse:
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
                    if split is None:
                        string = "NOTICE %s :I don't know that command\r\n" % (messageInfo['user'])
                        self.socket.send(string.encode('UTF-8'))
                    else:
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
                self.logIncomming(receivedData.encode('utf-8'))

    def logIncomming(self, stringToLog):
        #change eventually to log in a database but for now print is fine
        print(">> %s" % stringToLog)
    def logOutgoing(self, stringToLog):
        #change eventually to log in a database but for now print is fine
        print("<< %s" % stringToLog)
    def logError(self, stringToLog):
        print("!! %s" % stringToLog)
    def logInfo(self, stringToLog):
        print(".. %s" % stringToLog)

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


class ConfigurationError(Exception):
    pass


# So that the rest of this works, for now, parse the config file here and create ircBot
try:
    if os.path.isfile("irc-test.yaml"):
        with open("irc-test.yaml", 'r') as settings_file:
            conf = yaml.load(settings_file)
    else:
        with open("irc.yaml", 'r') as settings_file:
            conf = yaml.load(settings_file)
    # Print the configuration settings
    print("=== irc server ===")
    print("nick: " + conf['user']['nick'])
    print("pass: " + conf['user']['password'])
    print("chan: " + conf['channel']['name'])
    print("netw: " + conf['channel']['network'])
    print("port: " + str(conf['channel']['port']))

    print("=== database ==")
    print("db_name: " + conf['database']['name'])
    print("db_user: " + conf['database']['user'])
    print("db_pass: " + conf['database']['pass'])
    print("db_host: " + conf['database']['host'])
    print("db_port: " + str(conf['database']['port']))

    print("=== bot settings ===")
    print("cmd_pref: " + conf['settings']['prefix'])
    print("logAll:   " + str(conf['settings']['logAllToConsole']))
    print("respond:  " + str(conf['settings']['respondToNotFound']))

except FileNotFoundError:
    print("Config file not found. Make sure irc.yaml exists in this directory.")
    exit(1)

ircBot = IRCBot(conf)
