from core import ircBot, AddonBase 
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):
    def __init__(self):
      self.commandList = {
          "irc":self.irc,
          "reddit":self.reddit,
          "help":self.help,
          "wiki":self.wiki}
    
    def help(self, arguments, messageInfo):
      ircHelpers.sayInChannel("Welcome to progether! There may not always be a lot of activity here, just stick around. Someone will pop up. To experiment with the bot, try these commands: !!irc, !!reddit, !!wiki. Some future commands deal with chatlogs and in-channel mail.")

    def irc(self, arguments, messageInfo):
        ircHelpers.sayInChannel("server: irc.freenode.net, channel: #reddit-progether")
        
    def reddit(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://reddit.com/r/progether/")

    def wiki(self, arguments, messageInfo):
      ircHelpers.sayInChannel("http://www.reddit.com/r/progether/wiki/index")
