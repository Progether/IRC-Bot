from core import ircBot
import ircHelpers

@ircBot.registerCommand('say')
class Speak:
    def __init__(self):
        self.channel = ircHelpers.getChannel()
        
    def onRun(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (self.channel, messageInfo['user'] + ' told me to say ' + arguments)
        ircHelpers.send(command)
        
