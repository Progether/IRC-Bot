from core import ircBot
import ircHelpers

@ircBot.registerCommand('users')
class Speak:
    def __init__(self):
        self.ircHelper = ircHelpers
        self.channel = self.ircHelper.getChannel()
        
    def onRun(self, arguments):
        self.ircHelper.callForUsers()