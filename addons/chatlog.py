from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class ChatLog(AddonBase):
    prefix = ircBot.command_prefix

    help_description = ["Commands to review previous messages",]

    # All command groups should have a 'help_description' that explains the addon package. Help will take care of listing the commands.
    # Each command should have a help message to desc its usage. Register and assign help to command in 'self.helplist{}'
    help_lastlog  = ["%slastlog :: Says the last user's message in channel" % prefix]
    help_readlog   = ["%sreadlog :: Prints out the last chat log to a certain line amount ie: !!lastlog 50" % prefix]

    def __init__(self):
        self.commandList = {"lastlog" : self.lastMessage, "readlog" : self.readChatLog}
        self.messageList = [self.logMessage]
        self.helpList    = {'lastlog' : self.help_lastlog, 'readlog' : self.help_readlog }
        self.chatLog = list()

    def logMessage(self, messageInfo):
        self.chatLog.append(messageInfo)

    def lastMessage(self, arguments, messageInfo):
        ircHelpers.sayInChannel('%s said %s' % (self.chatLog[-1]['user'], self.chatLog[-1]['message']))

    def readChatLog(self, arguments, messageInfo):
        if arguments == '':
            index = -10
        else:
            index = int(int(arguments) / -1)
        while index <= -1:
            try:
                ircHelpers.privateMessage(messageInfo['user'], '%s: %s' % (self.chatLog[index]['user'], self.chatLog[index]['message']))
                index += 1
            except:
                index += 1

