from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):
    def __init__(self):
        self.channel = ircHelpers.getChannel()
        self.commandList = {"relay" : self.relay, "say" : self.speak }
        self.joinList = [self.sayHello]

    def sayHello(self, user):
        if user != ircHelpers.getNick():
            ircHelpers.sayInChannel("Hello %s! If you're new, try !!help" % user)

    def relay(self, arguments, messageInfo):
        if (len(arguments) <= 0):
            command = 'PRIVMSG %s :%s\r\n' % (messageInfo['channel'], messageInfo['user'] + ' told me to say nothing.')
        else:
            command = 'PRIVMSG %s :%s\r\n' % (messageInfo['channel'], messageInfo['user'] + ' told me to say ' + arguments)
        ircHelpers.send(command.encode("UTF-8"))
    
    def speak(self, arguments, messageInfo):
        ircHelpers.sayInChannel(arguments)
