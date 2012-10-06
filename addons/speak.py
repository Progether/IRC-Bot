from core import ircBot, AddonBase
import ircHelpers

import re

@ircBot.registerAddon()
class Speak(AddonBase):
    def __init__(self):
        self.channel = ircHelpers.getChannel()
        self.regex = re.compile(r":(?P<user>\w+)!~.+\sJOIN\s") 
	self.commandList = {"say" : self.speak}
	self.behaviourList = [self.sayHello]
	self.messageList = [self.message]

    def sayHello(self, data):
        match = self.regex.match(data)
        if match:
            if match.group('user') != ircHelpers.getNick():
                ircHelpers.sayInChannel('Hello %s!' % match.group('user'))        

    def speak(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (messageInfo['channel'], messageInfo['user'] + ' told me to say ' + arguments)
        ircHelpers.send(command)
        
    def message(self, messageInfo):
        ircHelpers.sayInChannel('Someone said something, was it you? %s!' % messageInfo['user'])
