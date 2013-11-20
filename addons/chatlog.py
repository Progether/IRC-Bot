from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class ChatLog(AddonBase):
    def __init__(self):
        self.commandList = {"lastlog" : self.lastMessage, "readlog" : self.readChatLog}
        self.messageList = [self.logMessage]
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
                
