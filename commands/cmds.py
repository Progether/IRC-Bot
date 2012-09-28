from core import ircBot
import ircHelpers

@ircBot.registerCommand('cmds')
class Reddit:
    def __init__(self):
        self.channel = ircHelpers.getChannel()

    def onRun(self, arguments, messageInfo):
        command = 'PRIVMSG %s :%s\r\n' % (self.channel, "http://en.wikipedia.org/wiki/List_of_Internet_Relay_Chat_commands")
        ircHelpers.send(command)
