from core import ircBot
import ircHelpers

@ircBot.registerCommand('join')
class Reddit:
    def __init__(self):
        self.channel = ircHelpers.getChannel()

    def onRun(self, arguments, messageInfo):
        command = 'JOIN %s \r\n' % arguments
        ircHelpers.send(command)
