from core import ircBot

@ircBot.registerCommand('say')
class Speak:
    def __init__(self, ircHelper):
        self.ircHelper = ircHelper

    def onRun(self, arguments):
        command = 'PRIVMSG %s :%s\r\n' % (self.ircHelper.channel, arguments)
        self.ircHelper.send(command)
        