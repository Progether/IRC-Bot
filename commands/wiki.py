from core import ircBot
import ircHelpers

@ircBot.registerCommand('wiki')
class Wiki:
    def __init__(self):
        self.channel = ircHelpers.getChannel()

    def onRun(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (messageInfo['channel'], "http://http://progether.wikia.com/wiki/Progether_Wiki/")
        ircHelpers.send(command)
        
