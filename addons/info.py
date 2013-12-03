from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class Speak(AddonBase):

    def __init__(self):
        help_description = ["Makes the bot post information for the channel."]

        help_irc  = ["%sirc :: server: irc.freenode.net, channel: #reddit-progether" % prefix]
        help_reddit  = ["%sreddit :: http://reddit.com/r/progether/" % prefix]
        help_nick = ["%snick :: gives information on a Nick" % prefix]
        help_wiki  = ["%swiki :: http://www.reddit.com/r/progether/wiki/index" % prefix]



        self.title = 'info'
        self.commandList = {
            "irc":self.irc,
            "reddit":self.reddit,
            "nick":self.changenick,
            "wiki":self.wiki}

        self.helpList    = {'irc' : self.help_irc, 'reddit' : self.help_reddit, "nick" : self.help_nick : "wiki" : self.help_wiki }



    def irc(self, arguments, messageInfo):
        ircHelpers.sayInChannel("server: irc.freenode.net, channel: #reddit-progether")

    def reddit(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://reddit.com/r/progether/")

    def wiki(self, arguments, messageInfo):
        ircHelpers.sayInChannel("http://www.reddit.com/r/progether/wiki/index")

    def changenick(self, arguments, messageInfo):
        ircHelpers.changeNick(arguments)
