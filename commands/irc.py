from core import ircBot

@ircBot.registerCommand('irc')
class IRC:
    def __init__(self, ircHelper):
        self.ircHelper = ircHelper

    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.ircHelper.channel, "server: irc.freenode.net, channel: #progether")
        self.ircHelper.send(command)
        
