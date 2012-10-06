from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):
    def __init__(self):
        self.channel = ircHelpers.getChannel()
	self.commandList = {"say" : self.speak}
	self.joinList = [self.sayHello]

    def sayHello(self, user):
        if user != ircHelpers.getNick():
            ircHelpers.sayInChannel('Hello %s!' % user)        

    def speak(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (messageInfo['channel'], messageInfo['user'] + ' told me to say ' + arguments)
        ircHelpers.send(command)
        
