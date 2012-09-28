from core import ircBot
import ircHelpers

@ircBot.registerCommand('faq')
class Faq:
    def __init__(self):
        self.channel = ircHelpers.getChannel()

    def onRun(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (self.channel, "http://code.reddit.com/wiki/help/faqs/progether")
        ircHelpers.send(command)
        
