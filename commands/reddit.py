from core import ircBot

@ircBot.registerCommand('reddit')
class Reddit:
    def __init__(self, ircHelper):
        self.ircHelper = ircHelper

    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.ircHelper.channel, "http://reddit.com/r/progether/")
        self.ircHelper.send(command)
        
