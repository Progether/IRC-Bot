from core import ircBot
import ircHelpers

@ircBot.registerCommand('irc')
class IRC:
    def __init__(self):
        self.channel = ircHelpers.getChannel()

    def onRun(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (self.channel, "server: irc.freenode.net, channel: #reddit-progether")
        ircHelpers.send(command)
        
