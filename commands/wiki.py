from core import ircBot

@ircBot.registerCommand('wiki')
class Wiki:
    def __init__(self, ircHelper):
        self.ircHelper = ircHelper

    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.ircHelper.channel, "http://http://progether.wikia.com/wiki/Progether_Wiki/")
        self.ircHelper.send(command)
        
