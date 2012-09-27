from core import ircBot
import ircHelpers

@ircBot.registerCommand('git')
class Git:
    def __init__(self):
        self.channel = ircHelpers.getChannel()

    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.channel, "https://github.com/Progether")
        ircHelpers.send(command)
        
