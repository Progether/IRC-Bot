import socket, re

from commandModule import CommandModule
from ircHelpers import IRCHelper

class IRCBot:
    def __init__(self, network, port, channel, nickname, tempCacheSize=4096):
        self.network = network
        self.port = port
        self.channel = channel
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.tempCacheSize = tempCacheSize

        self.ircHelper = IRCHelper(self)

        self.commandModule = CommandModule(self.ircHelper)
        self.regexIsCommand = re.compile(r".*(?P<command>!!.*)")



    def run(self):
        self.socket.connect((self.network, self.port))
        self.log(self.socket.recv(self.tempCacheSize))
        self.socket.send('NICK %s \r\n' % self.nickname)
        self.socket.send('USER %s some stuff :Python IRC\r\n' % self.nickname)#change this
        self.socket.send('JOIN %s \r\n' % self.channel)
        self.mainLoop()

    def mainLoop(self):
        while True:
            recievedData = self.socket.recv(self.tempCacheSize)
            self.log(recievedData)

            isCommand = self.regexIsCommand.match(recievedData)
            if isCommand:
                self.commandModule.runCommand(isCommand.group('command'))
            
            #temporary quit method, should be changed so only admins can use
            if recievedData.find('!!quit') != -1:
                self.log("Quitting")
                self.socket.send('QUIT\r\n')
                break
            
            #make sure we don't time out of server
            if recievedData.find('PING') != -1:
                self.socket.send('PONG %s \r\n' % recievedData.split()[1])

    def log(self, stringToLog):
        #change eventually to log in a file but for now print is fine
        print stringToLog

ircbot = IRCBot('irc.freenode.net', 6667, '#progether', 'WorkingIRCBot')
ircbot.run()
