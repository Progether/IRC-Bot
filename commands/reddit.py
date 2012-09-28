from core import ircBot
import ircHelpers

@ircBot.registerCommand('reddit')
class Reddit:
    def __init__(self):
        self.channel = ircHelpers.getChannel()

    def onRun(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (self.channel, "http://reddit.com/r/progether/")
        ircHelpers.send(command)
        
