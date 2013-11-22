from core import ircBot, AddonBase 
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):
    
    def __init__(self):
        self.title = 'info'
        self.commandList = {
            "irc":self.irc,
            "reddit":self.reddit,
            "nick":self.changenick,
            "wiki":self.wiki}
    

    def irc(self, arguments, messageInfo):
        ircHelpers.sayInChannel("server: irc.freenode.net, channel: #reddit-progether")
        
    def reddit(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://reddit.com/r/progether/")

    def wiki(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://www.reddit.com/r/progether/wiki/index")

    def changenick(self, arguments, messageInfo):
        ircHelpers.changeNick(arguments)
