from core import ircBot

@ircBot.registerCommand('faq')
class Faq:
    def __init__(self, ircHelper):
        self.ircHelper = ircHelper

    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.ircHelper.channel, "http://code.reddit.com/wiki/help/faqs/progether")
        self.ircHelper.send(command)
        
