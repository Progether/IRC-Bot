from core import ircBot, AddonBase 
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):
    def __init__(self):
	self.commandList = {"faq":self.faq,
			"git":self.git,
			"irc":self.irc,
			"reddit":self.reddit,
			"wiki":self.wiki}

    def faq(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://code.reddit.com/wiki/help/faqs/progether")
 
    def git(self, arguments, messageInfo):
        ircHelpers.sayInChannel("https://github.com/Progether")
        
    def irc(self, arguments, messageInfo):
        ircHelpers.sayInChannel("server: irc.freenode.net, channel: #progether")
        
    def reddit(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://reddit.com/r/progether/")

    def wiki(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://http://progether.wikia.com/wiki/Progether_Wiki/")
