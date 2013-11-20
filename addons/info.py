from core import ircBot, AddonBase 
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):
    def __init__(self):
      self.commandList = {
          "irc":self.irc,
          "reddit":self.reddit,
          "help":self.help,
          "mailhelp":self.mailhelp,
          "projecthelp":self.projecthelp,
          "wiki":self.wiki}
    
    def help(self, arguments, messageInfo):
        ircHelpers.sayInChannel("Welcome to progether! There may not always be a lot of activity here, just stick around. Someone will pop up. To experiment with the bot, try these commands: !!irc, !!reddit, !!wiki, !!mailhelp, !!projecthelp. Some future commands deal with chatlogs. All commands can be done as private messages: /msg progether !!<command>.")

    def mailhelp(self, arguments, messageInfo):
        ircHelpers.sayInChannel("To view mail: !!mymail. To send mail: !!mail <recipient> <message>. To delete mail: !!delmail <id>.")

    def projecthelp(self, arguments,messageInfo):
        ircHelpers.sayInChannel("To view all projects: !!projects. To add a project: !!addproject <name> <language> <description>. To delete a project: !!delproject <id>. Name and programming languages should not contain spaces.")

    def irc(self, arguments, messageInfo):
        ircHelpers.sayInChannel("server: irc.freenode.net, channel: #reddit-progether")
        
    def reddit(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://reddit.com/r/progether/")

    def wiki(self, arguments, messageInfo):
      ircHelpers.sayInChannel("http://www.reddit.com/r/progether/wiki/index")
