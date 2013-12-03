from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):
    def __init__(self):

        help_description = ["Commands to make the bot say something in channel."]

        help_speak  = ["%sspeak :: No description found" % prefix]
        help_say  = ["%ssay :: Says typed text into channel" % prefix]
        help_relay  = ["%srelay :: Relays a message from bot to channel." % prefix]


        self.title = 'speak'
        self.channel = ircHelpers.getChannel()
        self.commandList = {"relay" : self.relay, "say" : self.speak }
        self.helpList    = {'relay' : self.help_relay, 'say' : self.help_say, "speak" : self.help_speak}
        self.joinList = [self.sayHello]

    def sayHello(self, user):
        if user != ircHelpers.getNick():
            ircHelpers.pmInChannel(user, "Hello %s! If you're new, try !!help" % user)

    def relay(self, arguments, messageInfo):
        if (len(arguments) <= 0):
            command = 'PRIVMSG %s :%s\r\n' % (messageInfo['channel'], messageInfo['user'] + ' told me to say nothing.')
        else:
            command = 'PRIVMSG %s :%s\r\n' % (messageInfo['channel'], messageInfo['user'] + ' told me to say ' + arguments)
        ircHelpers.send(command.encode("UTF-8"))

    def speak(self, arguments, messageInfo):
        ircHelpers.sayInChannel(arguments)
