from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class Helper(AddonBase):
    
    '''
      Set help messages for commands within their own classes. Refer to 'mail.py' for an example of how to properly implement it.
      All messages must be lists of Strings. Each separate String will get printed on a new line when passed to user/channel.
      
      If no help is found for a command argument (either no command exists or no help found) applicable 'HELP_NONE_' variant is selected.
    '''
    ##TODO enforce help in AddonBase
    ##TODO public method for sending help/usage to a user from within other addons
    
    # static strings
    CASE_ALL     = ('all',)              # used to get help for all commands
    CASE_CMDS    = ('commands', 'cmds')  # used to get commands for all addon packages
    CASE_STARTER = ('start',)            # suggest a couple of commands to try
    
    MODIFIER_LONG    = ('long', 'verbose')   # give the extended version of the help
    MODIFIER_CHANNEL = ('channel', 'chan')   # used to send response to channel instead of a user
    
    PREFIX = ircBot.command_prefix
    INDENT = "  "        # for formatting the output
    
    # defaults if no help exists or encountered error
    NONE_LONG   = ("Sorry, we don't have any help for that command. Make sure you spelled it correctly or slap the dev for not including it",)
    NONE_SHORT = ("No help found.",)
    NONE_DESCR_LONG  = ("No description has been supplied. Maybe the developer didn't have enough coffee that morning?",)
    NONE_DESCR_SHORT = ("No description for this package. Shame on you dev, shame.",)
    NONE_CMDS  = ("Unable to access some or all of this addon's commands. Sorry  about that.",
                       "{0}Perhaps you'd like to patch it for us??".format(INDENT))
    
    # main help message - response to bare 'help' command
    HELP_ROOT = ("Welcome to progether! There may not always be a lot of activity here, just stick around. IRC use requires some patience",
                "All commands for the bots can also be done as private messages: /msg {0} {1}<command>.".format(ircBot.nickname, PREFIX))
    
    HELP_VERBOSE = ("This is the long help for the {0}help command. Sorry the length but there's a few things you need to know"
                                                    .format(PREFIX),
                    "{0}As mentioned the root command is '{1}help'. It can be used on it's own but its power comes from arguments"
                                                    .format(Helper.INDENT, PREFIX),
                    "{0}The advanced usage is: '{1}help [modifier] [command or addon]"
                                                    .format(Helper.INDENT, PREFIX),
                    "{0}{0}(Modifiers)  long: extended help and descriptions, channel: redirect output".format(PREFIX),
                    "{0}{0}(Commands/Addons) Any available command or addon title" )
    
    HELP_START = ("Looking for something to do? Try running a '{0}help {1}' or '{0}help {2}' command"
                                                    .format(PREFIX, Helper.CASE_ALL, Helper.CASE_CMDS),)
    
    HELP_INTRO = ("Welcome to progether, a reddit born collection of programmers teaching each other how not to do things.",
                 "{0}Here's what this bot can do:".format(INDENT))
    
    # required description messages for this addon
    help_description_short = ("Get help on the bot's functionality",)
    help_description_long  = ("Addon to delve into the other addons and functionality on offer. Try '{0}help {1} {2}' to see it all"
                                                    .format(PREFIX, Helper.MODIFIER_LONG[0], Helper.CASE_ALL[0]),)
    # required command descriptions (assigned in self.helpList{})
    help_help     = ("{0}help [modifier] [addon/command] :: Get help on bot's commands. For full usages: '{0}help verbose'"
                                                    .format(PREFIX),)
    help_help_aid = ("{0}aid [user] [addon/command] :: Send help to another user. Usage is the same as for {0}help. See '{0}help verbose' for details"
                                                    .format(PREFIX),)
    
    
    
    ### init and command functions
    
    def __init__(self):
        self.title = 'helper'
        self.commandList = { 'help' : self.help,       'aid' : self.aid      }
        self.helpList    = { 'help' : Helper.help_help,  'aid' : Helper.help_aid }
        

    '''DONE'''
    def help(self, arguments, messageInfo):
        user = messageInfo['user']
        args = arguments.split()
        
        self.__giveHelp(user, args)
            
    '''DONE'''
    def aid(self, arguments, messageInfo):
        args = arguments.split()
        requesting_user = messageInfo['user']
        
        if len(args) == 0:
            help_messages = self.__getCommandHelpFromAddon(self.title, 'aid', False, False)
            self.__sayToUser(requesting_user, help_messages)
        else:
            target_user = args.pop(0)
            announce_aid_msg = ('{0} thinks {1} needs some help'.format(requesting_user, target_user),)
            self.__sayToChannel(announce_aid_msg)
            self.__giveHelp(target_user, args, False)
        
            
    ### function that does the heavy lifting. can be called recursively for changing target of the help (or other)
    def __giveHelp(self, user, split_arguments, useShortFormat=True, times_run=0):
        if times_run > 5:
            print("!! Too many recursive calls to Help.__giveHelp(). Giving up.")
            return
        
        num_args = len(split_arguments)
        
        # bare 'help' command on its own
        if num_args == 0:                        
            self.__sayDefaultToUser(user, useShortFormat)

        # has arguments we need to parse
        else:
            first_arg = split_arguments[0].lower()
            
            # display all help at once:
            if first_arg in Helper.CASE_ALL:
                if num_args > 1 and split_arguments[1].lower() in Helper.MODIFIER_LONG:
                    help_messages = self.__getAllHelp(False)
                else:
                    help_messages = self.__getAllHelp(True)
                self.__sayToUser(user, help_messages)
            
            # list all commands available in short form (for recap):
            elif first_arg in Helper.CASE_CMDS:
                help_messages = self.__getAllCompactAddonHelp()
                self.__sayToUser(user, help_messages)
            
            # send output to channel:
            elif first_arg in Helper.MODIFIER_CHANNEL:
                split_arguments.pop(0)      # remove channel command and restart parse
                help_messages = self.__getHelp(split_arguments)
                self.__sayToChannel(help_messages)
            
            elif first_arg in Helper.MODIFIER_LONG:
                split_arguments.pop(0)      # remove verbose modifier before recursing back
                if len(split_arguments) == 0:
                    self.__giveHelp(user, list(), False, times_run+1)
                else:
                    self.__giveHelp(user, split_arguments, False, times_run+1)
            
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
        help_messages = Helper.HELP_ALL_INTRO
        addons = ircBot.addonList
        for addon in addons:
            help_messages = help_messages + self.__getFullAddonHelp(addon, useShortFormat)
        return help_messages

    '''DONE'''
    def __getFullAddonHelp(self, addon, useShortFormat=True):
        messages = self.__getAddonIntro(addon, useShortFormat)
        try:
            for cmd in addon.commandList:
                messages = messages + self.__getCommandHelpFromAddon(addon, cmd, useShortFormat, True)
        except (AttributeError):
            messages = messages + Helper.NONE_CMDS
        return messages
    
    '''DONE, CORRECT'''
    def __getAllCompactAddonHelp(self):
        help_messages = tuple()
        for addon in ircBot.addonList:
            help_messages.__add__(self.__getCompactAddonHelp(addon))
        return help_messages
        
    
    '''DONE, CORRECT'''
    def __getCompactAddonHelp(self, addon):
        messages = self.__getAddonIntro(addon, True)
        cmds_summary = "{}Available commands: ".format(Helper.INDENT)
        try:
            for cmd in addon.commandList:
                cmds_summary.__add__("{0}{1}, ".format(Helper.PREFIX, cmd))
        except (AttributeError):
            pass
        return messages.__add__((cmds_summary,))
    
    ### addon info extracty functions
    
    '''DONE'''
    def __getAddonIntro(self, addon, useShortFormat=True):
        title = self.__getAddonTitle(addon)
        desc  = self.__getAddonDescription(addon, useShortFormat)
        msg = "{0} :: {1}"
        return (msg.format(title, desc),)
    
    '''DONE, CORRECT'''
    def __getAddonTitle(self, addon):
        try:
            title = addon.title
        except AttributeError:
            title = addon.__class__.__name__
        return title
    
    '''DONE, CORRECT'''
    def __getAddonDescription(self, addon, useShortFormat=True):
        desc = None
        try:
            if useShortFormat:
                desc = addon.help_description_short
            else:
                desc = addon.help_description_long
        except AttributeError:
            if useShortFormat:
                desc = Helper.NONE_DESCR_SHORT
            else:
                desc = Helper.NONE_DESCR_LONG
        return desc
    
    ### command help extracty functions
    
    
    def __getCommandHelpFromAddon(self, addon, command, useShortFormat=True, isChildComment=False):
        desc = None
        try:
            if command in addon.addonList:
                desc = addon.helpList['command']
        except (AttributeError, KeyError):
            pass
        if not desc:
            return self.__makeCommandNoneMessage(command, useShortFormat, isChildComment)
        else:
            msg = "{0}{1} :: {2}".format(Helper.PREFIX, command, desc)
            return (msg,)
            
    
    
    
    ### formatting functions
    
    '''DONE'''
    def __makeCommandNoneMessage(self, command, useShortFormat=True, isChildComment=True):
        msg = "{1}{2} :: {3}"
        if isChildComment:
            msg = Helper.INDENT + msg
        if useShortFormat:
            return (msg.format(Helper.PREFIX, command, Helper.NONE_SHORT),)
        else:
            return (msg.format(Helper.PREFIX, command, Helper.NONE_LONG),)
    
    '''DONE, CORRECT, UNUSED'''
    def __makeInvokeCommand(self, command, useShortFormat=True, **args):
        if useShortFormat:
            msg = "Read more:"
        else:
            msg = "For a more in depth explanation use:"
        cmdToInvoke = "{0}{1}".format(Helper.PREFIX, command)
        if args:
            for arg in args:
                cmdToInvoke = "{0} {1}".format(cmdToInvoke, arg)
        return ("{0} {1}".format(msg, cmdToInvoke),)
    
    
    ### speak functions:
    
    '''DONE, CORRECT'''
    def __sayToChannel(self, help_messages, **channels):
        ##TODO write handling for multi-channel
        for message in help_messages:
            ircHelpers.sayInChannel(message)
    
    '''DONE, CORRECT'''
    def __sayToUser(self, user, help_messages):
        for message in help_messages:
            ircHelpers.pmInChannel(user, message)
    
    '''DONE, CORRECT'''
    def __sayDefaultToUser(self, user, useShortFormat=True):
        if useShortFormat:
            self.__sayToUser(user, Helper.HELP_ROOT)
        else:
            self.__sayToUser(user, Helper.HELP_VERBOSE)
                    #
                    #
    help_project = "To view all projects: !!projects. To add a project: !!addproject <name> <language> <description>. " \
                   +"To delete a project: !!delproject <id>. Name and programming languages should not contain spaces."        