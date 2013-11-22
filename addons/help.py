from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class Help(AddonBase):
    
    '''
      Set help messages for commands within their own classes. Refer to 'mail.py' for an example of how to properly implement it. ##TODO enforce help in AddonBase
      All messages must be lists of Strings. Each separate String will get printed on a new line when passed to user/channel.
      
      If no help is found for a command argument (either no command exists or no help found) applicable 'HELP_NONE_' variant is selected.
    '''
    
    ### static strings
    HELP_MODIFIER_ALL     = ('all',)              # used to get help for all commands
    HELP_MODIFIER_CMDS    = ('commands', 'cmds')  # used to get commands for all addon packages
    HELP_MODIFIER_START   = ('start',)            # suggest a couple of commands to try
    
    HELP_MODIFIER_LONG    = ('long', 'verbose')   # give the extended version of the help
    HELP_MODIFIER_CHANNEL = ('channel', 'chan')   # used to send response to channel instead of a user
    
    HELP_INDENT           = "  "        # for formatting the output
    
    ### default if no help exists
    HELP_NONE_LONG  = ("Sorry, we don't have any help for that command. Make sure you spelled it correctly or slap the dev for not including it",)
    HELP_NONE_SHORT = ("No help found.",)
    HELP_NONE_DESCR_LONG  = ("No description has been supplied. Maybe the developer didn't have enough coffee that morning?",)
    HELP_NONE_DESCR_SHORT = ("No description for this package. Shame on you dev, shame.")
    
    ### main help message - response to bare 'help' command
    HELP_ROOT = ("Welcome to progether! There may not always be a lot of activity here, just stick around. IRC use requires some patience",
                "All commands for the bots can also be done as private messages: /msg {0} {1}<command>.".format(ircBot.nickname, ircBot.command_prefix))
    HELP_START = ("Looking for something to do? Try running a '{0}help {1}' or '{0}help {2}' command".format(
                                                                ircBot.command_prefix, Help.HELP_MODIFIER_ALL, Help.HELP_MODIFIER_CMDS),)
    HELP_INTRO = ("Welcome to progether, a reddit born collection of programmers teaching each other how not to do things.",
                 "{0}Here's what this bot can do:".format(HELP_INDENT))
    
    
    def __init__(self):
        self.title = 'help'
        self.commandList = { 'help' : self.help,       'aid' : self.aid      }
        self.helpList    = { 'help' : Help.help_help,  'aid' : Help.help_aid }


    def help(self, arguments, messageInfo):
        user = messageInfo['user']
        args = arguments.split()
        
        self.__giveHelp(user, args)
            
    
    
    def aid(self, arguments, messageInfo):
        pass

    
    def __giveHelp(self, user, split_arguments, times_run=0):
        num_args = len(split_arguments)
        
        # bare 'help' command on its own
        if num_args == 0:                        
            self.__sayDefaultToUser(user)

        # has arguments we need to parse
        else:
            first_arg = split_arguments[0].lower()
            
            # display all help at once:
            if first_arg in Help.HELP_MODIFIER_ALL:
                if num_args > 1 and split_arguments[1].lower() in Help.HELP_MODIFIER_LONG:
                    help_messages = self.__getAllHelp(False)
                else:
                    help_messages = self.__getAllHelp(True)
                self.__sayToUser(user, help_messages)
            
            # list all commands available in short form (for recap):
            elif first_arg in Help.HELP_MODIFIER_CMDS:
                pass
            
            # send output to channel:
            elif first_arg in Help.HELP_MODIFIER_CHANNEL:
                split_arguments.pop(0)      # remove channel command and restart parse
                help_messages = self.__getHelp(split_arguments)
                self.__sayToChannel(help_messages)
            
            elif first_arg in Help.HELP_MODIFIER_LONG:
                pass
            # otherwise parse argument as a command
            else:
                help_messages = self.__getHelp(split_arguments)
        
    
    ### top level help compilation functions
    
    '''DONE'''
    def __getHelpOnSingleCmd(self, command):
        addons = ircBot.addonList
        for addon in addons:
            try:
                if command == addon.title:
                    return self.__getAddonHelpLong(addon)
            except AttributeError:
                pass
            try:
                if command in addon.commandList:
                    return self.__getCommandHelpFromAddon(addon, command, False, False)
            except (AttributeError, KeyError):
                pass
            return self.__makeCommandNoneMessage(command, False, False)
    
    def __getHelp(self, arguments):
        # parse arguments for normal commands, return help_messages
        # determine long or short format based on what it is. cmd = long, addon = short
        pass
    
    '''DONE'''
    def __getAllHelp(self, useShortFormat=True):
        help_messages = Help.HELP_ALL_INTRO
        addons = ircBot.addonList
        for addon in addons:
            help_messages = help_messages + self.__getFullAddonHelp(addon, useShortFormat)
        return help_messages


    def __getFullAddonHelp(self, addon, useShortFormat=True):
        messages = self.__getAddonIntro(addon, useShortFormat)
        for cmd in addon.commandList:
            messages = messages + self.__getAddonIntro(addon, useShortFormat)
    
    def __getAllCompactAddonHelp(self, addon):
        pass
    
    ### addon info extracty functions
    
    '''DONE'''
    def __getAddonIntro(self, addon, useShortFormat=True):
        title = self.__getAddonTitle(addon)
        desc  = self.__getAddonDescription(addon, useShortFormat)
        msg = "{0} :: {1}"
        return (msg.format(title, desc),)
    
    '''DONE'''
    def __getAddonTitle(self, addon):
        try:
            title = addon.title
        except AttributeError:
            title = addon.__class__.__name__
        return title
    
    '''DONE'''
    def __getAddonDescription(self, addon, useShortFormat=True):
        desc = None
        try:
            if useShortFormat:
                desc = addon.help_description_short
            else:
                desc = addon.help_description_long
        except AttributeError:
            pass
        if not desc:
            if useShortFormat:
                desc = Help.HELP_NONE_DESCR_SHORT
            else:
                desc = Help.HELP_NONE_DESCR_LONG
        return desc
    
    ### command help extracty functions
    
    def __getCommandHelpFromAddon(self, addon, command, useShortFormat=True, isChildComment=False):
        desc = None
        try:
            for cmd in addon.commandList:
                if command == cmd:
                    desc = addon.helpList['cmd']
        except (AttributeError, KeyError):
            pass
        if not desc:
            return self.__makeCommandNoneMessage(command, useShortFormat, isChildComment)
        else:
            msg = "{0}{1} :: {2}".format(ircBot.command_prefix, command, desc)
            return (msg,)
            
    
    
    
    ### formatting functions
    
    '''DONE'''
    def __makeCommandNoneMessage(self, command, useShortFormat=True, isChildComment=True):
        msg = "{1}{2} :: {3}"
        if isChildComment:
            msg = Help.HELP_INDENT + msg
        if useShortFormat:
            return (msg.format(ircBot.command_prefix, command, Help.HELP_NONE_DESCR_SHORT),)
        else:
            return (msg.format(ircBot.command_prefix, command, Help.HELP_NONE_DESCR_LONG),)
    
    '''DONE'''
    def __makeInvokeCommand(self, command, useShortFormat=True, **args):
        if useShortFormat:
            msg = "Read more: "
        else:
            msg = "For a more in depth explanation use: "
        cmdToInvoke = "{0}{1}".format(ircBot.command_prefix, command)
        if args:
            for arg in args:
                cmdToInvoke = "{0} {1}".format(cmdToInvoke, arg)
        return ("{0}{1}".format(msg, cmdToInvoke),)
    
    
    ### speak functions:
    
    '''DONE'''
    def __sayToChannel(self, help_messages, **channels):
        for message in help_messages:
            ircHelpers.sayInChannel(message)
    
    '''DONE'''
    def __sayToUser(self, user, help_messages):
        for message in help_messages:
            ircHelpers.pmInChannel(user, message)
    
    '''DONE'''
    def __sayDefaultToUser(self, user):
        self.__sayToUser(user, Help.help_root)
                    
    help_project = "To view all projects: !!projects. To add a project: !!addproject <name> <language> <description>. " \
                   +"To delete a project: !!delproject <id>. Name and programming languages should not contain spaces."        