from core import ircBot

@ircBot.registerCommand('git')
class Git:
    def __init__(self, ircHelper):
        self.ircHelper = ircHelper

    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.ircHelper.channel, "https://github.com/Progether")
        self.ircHelper.send(command)
        
