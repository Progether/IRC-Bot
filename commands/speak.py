from core import ircBot
import ircHelpers

@ircBot.registerCommand('say')
class Speak:
    def __init__(self):
        self.channel = ircHelpers.getChannel()
        
    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.channel, arguments)
        ircHelpers.send(command)
        
