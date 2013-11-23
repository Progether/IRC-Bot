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
    CASE_ALL     = ('all', 'a')              # used to get help for all commands
    CASE_CMDS    = ('commands', 'cmds')      # used to get commands for all addon packages
    CASE_ADDONS  = ('addons', 'add')         # explain all the addon packages
    CASE_STARTER = ('start', 's')            # suggest a couple of commands to try
    
    MODIFIER_LONG    = ('verbose', 'long', 'v')   # give the extended version of the help
    MODIFIER_CHANNEL = ('channel', 'chan', 'c')   # used to send response to channel instead of a user
    
    PREFIX = ircBot.command_prefix  # to construct command examples
    INDENT = "  "                   # for formatting the output
    
    # defaults if no help exists or encountered error
    NONE_CMD_LONG    = ["Sorry, we don't have any help for this command. Make sure you spelled it correctly or slap the dev for not including it",]
    NONE_CMD_SHORT   = ["No help found. I'll try harder next time.",]
    NONE_DESCR_LONG  = ["No description has been supplied. Maybe the developer didn't have enough coffee that morning?",]
    NONE_DESCR_SHORT = ["No description for this package. Shame on you dev, shame.",]
    NONE_CMDS  = ["Unable to access some or all of this addon's commands. Sorry  about that.",
                  "{0}Perhaps you'd like to patch it for us??".format(INDENT)]
    
    # main help message - response to bare 'help' command
    HELP_ROOT = ["Welcome to progether! There may not always be a lot of activity here, just stick around. IRC use requires some patience",
                 "{0}All commands for the bots can also be done by private messages: /msg {1} {2}[command] [**args]".format(INDENT, ircBot.nickname, PREFIX),
                 "{0}For a longer explanation use: '{1}help {2}'".format(INDENT, PREFIX, MODIFIER_LONG[0])]
    
    HELP_VERBOSE = ["This is the long help for the {0}help command. Sorry the length but there's a few things you need to know"
                                                    .format(PREFIX),
                    "{0}As mentioned the root command is '{1}help'. It can be used on it's own but its power comes from arguments"
                                                    .format(INDENT, PREFIX),
                    "{0}The help command usage is: '{1}help [Modifier] [Case] [Command / Addon Title]'"
                                                    .format(INDENT, PREFIX),
                    "{0}{0}(Modifiers)  'verbose': extended info, 'channel': redirect output, ''".format(INDENT),
                    "{0}{0}(Cases)  'start', 'commands', 'addons' - try them. Using a 'Case' will ignore 'Command'".format(INDENT),
                    "{0}{0}(Commands/Addons)  Any available Command or Addon Title. Try 'addons' Case to start off".format(INDENT) ]
    
    HELP_START   = ["Looking for something to play with? Try running a '{0}help {1}' or '{0}help {2}' command"
                                                    .format(PREFIX, CASE_ADDONS[0], CASE_CMDS[0]),]
    
    HELP_INTRO   = ["Welcome to progether, a reddit born collection of programmers teaching each other how not to do things.",
                   "{0}Here's what this bot can do:".format(INDENT) ]
    
    HELP_ADDONS  = ["These are the currently active addon packages. For details of the commands within any of them try:",
                    "{0}Addon explore command: {1}help [addon_title]".format(INDENT, PREFIX)]
    
    # required description messages for this addon
    help_description_short = ["Get help on the bot's functionality",]
    help_description_long  = ["Addon to delve into the other addons and functionality on offer. Try '{0}help {1} {2}' to see it all"
                                                    .format(PREFIX, MODIFIER_LONG[0], CASE_ALL[0]),]
    # required command descriptions (assigned in self.helpList{})
    help_help     = ["{0}help [modifier] [addon/command] :: Get help on bot's commands. For full usages: '{0}help verbose'"
                                                    .format(PREFIX),]
    help_aid = ["{0}aid [user] [help arguments] :: Send help to another user. Usage is the same as for {0}help. See '{0}help verbose' for details"
                                                    .format(PREFIX),]
    
    
    
    ### init and command functions
    
    def __init__(self):
        self.debug = False    # for debugging, logs actions and flow to console
        self.title = 'helper'
        self.commandList = { 'help' : self.help,       'aid' : self.aid      }
        self.helpList    = { 'help' : self.help_help,  'aid' : self.help_aid }
        

    def help(self, arguments, messageInfo):
        user = messageInfo['user']
        args = arguments.split()
        
        if self.debug: print("== Begin 'help'. args: %d" % len(args)) 
        
        self.__giveHelp(user, args)
            
            
    def aid(self, arguments, messageInfo):
        args = arguments.split()
        requesting_user = messageInfo['user']
        
        # can't use without args so give them the help for the command
        if len(args) == 0:
            help_messages = self.__getCommandHelpFromAddon(self.title, 'aid', False, False)
            self.__sayToUser(requesting_user, help_messages)
        else:
            ##TODO Perform test for user online and known to bot
            target_user = args.pop(0)
            announce_aid_msg = ('{0} thinks {1} needs some help'.format(requesting_user, target_user),)
            self.__sayToChannel(announce_aid_msg)
            self.__giveHelp(target_user, args, False)
        
            
    ### function that does the heavy lifting. can be called recursively for changing target of the help (or other)
    def __giveHelp(self, user, split_arguments, useShortFormat=True, times_run=0, sendToChannel=False):
        if times_run > 5:
            print("!! Too many recursive calls to Help.__giveHelp(). Giving up.")
            return
        
        num_args = len(split_arguments)
        
        # bare 'help' command on its own
        if num_args == 0:               
            if self.debug: print("== No args, giving default")
            if sendToChannel:
                self.__sayDefaultToChannel(useShortFormat)
            else:
                self.__sayDefaultToUser(user, useShortFormat)

        # has arguments we need to parse
        else:
            first_arg = split_arguments[0].lower()
            
            # display all help at once:
            if first_arg in Helper.CASE_ALL:
                if self.debug: print("== Found CASE_ALL")
                if num_args > 1 and split_arguments[1].lower() in Helper.MODIFIER_LONG:
                    help_messages = self.__getAllHelp(False)
                else:
                    help_messages = self.__getAllHelp(True)
                if sendToChannel:
                    self.__sayToChannel(help_messages)
                else:
                    self.__sayToUser(user, help_messages)
            
            # list all addon packages and descriptions
            elif first_arg in Helper.CASE_ADDONS:
                if self.debug: print("== Found CASE_ADDONS")
                help_messages = self.__getAllAddonDescriptions(False)
                if sendToChannel:
                    self.__sayToChannel(help_messages)
                else:
                    self.__sayToUser(user, help_messages)
                
            # list all commands available in short form (for recap):
            elif first_arg in Helper.CASE_CMDS:
                if self.debug: print("== Found CASE_CMDS")
                help_messages = self.__getAllCompactAddonHelp()
                if sendToChannel:
                    self.__sayToChannel(help_messages)
                else:
                    self.__sayToUser(user, help_messages)
            
            # send output to channel:
            elif first_arg in Helper.MODIFIER_CHANNEL:
                if self.debug: print("== Found MOD_CHANNEL")
                split_arguments.pop(0)      # remove channel command and restart parse
                self.__giveHelp(ircBot.channel, split_arguments, useShortFormat, times_run+1, sendToChannel=True)
                
            # set long descriptions True and call again recursively (or server HELP_VERBOSE if no args)
            elif first_arg in Helper.MODIFIER_LONG:
                if self.debug: print("== Found MOD_VERBOSE")
                split_arguments.pop(0)      # remove verbose modifier before recursing back
                if len(split_arguments) == 0:
                    self.__giveHelp(user, list(), False, times_run+1, sendToChannel)
                else:
                    self.__giveHelp(user, split_arguments, False, times_run+1, sendToChannel)
            
            # otherwise parse argument as a command
            else:
                if self.debug: print("== No mods left. Parse cmd: " +split_arguments[0])
                help_messages = self.__getHelpForSingleCmd(split_arguments[0])
                if sendToChannel:
                    self.__sayToChannel(help_messages)
                else:
                    self.__sayToUser(user, help_messages)
        
    
    ### top level help compilation functions
    
    def __getHelpForSingleCmd(self, command):
        command = command.lower()
        addons = ircBot.addonList[:]
        if self.debug: print("== Num of loaded addons: %d" % len(addons))
        for addon in addons:
            try:
                test_title = self.__getAddonTitleStr(addon)
                if command == test_title:
                    if self.debug: print("== Matched with title: %s" % test_title)
                    return self.__getFullAddonHelp(addon, False)
            except (AttributeError) as e:
                if self.debug: print("== AttrError in getHelpOnSingleCmd() - title\r\n", e.args[0])
            try:
                if command in addon.commandList.keys():
                    if self.debug: print("== Found cmd in addonList keys: %s" % self.__getAddonTitleStr(addon))
                    return self.__getCommandHelpFromAddon(addon, command, False, False)
            except (AttributeError, KeyError) as e:
                if self.debug: print("== Attr/KeyError in getHelpOnSingleCmd() - cmdList\r\n", e.args[0])
        if self.debug: print("== serving default cmd missing")
        return self.__makeCommandNoneMessage(command, False, False)
    

    def __getAllHelp(self, useShortFormat=True):
        help_messages = Helper.HELP_INTRO
        addons = ircBot.addonList[:]
        for addon in addons:
            help_messages.extend(self.__getFullAddonHelp(addon, useShortFormat))
        return help_messages


    def __getFullAddonHelp(self, addon, useShortFormat=True):
        help_messages = self.__getAddonIntro(addon, useShortFormat)
        help_messages.extend(self.__getAllCommandsHelpFromAddon(addon, useShortFormat))
        return help_messages
    

    def __getAllCompactAddonHelp(self):
        help_messages = []
        addons = ircBot.addonList[:]
        for addon in addons:
            help_messages.extend(self.__getCompactAddonHelp(addon))
        return help_messages


    def __getCompactAddonHelp(self, addon):
        help_messages = self.__getAddonIntro(addon, True)
        cmds_summary = "{}Available commands: ".format(Helper.INDENT)
        try:
            for cmd in addon.commandList:
                cmds_summary = "{0}{1}".format(cmds_summary, "{0}{1}, ".format(Helper.PREFIX, cmd)).rstrip(', ')
        except (AttributeError):
            if self.debug: print("== AttrErr in getCompactAddonHelp")
        help_messages.extend((cmds_summary,))
        return help_messages
    
    ### addon info extracty functions
    

    def __getAddonIntro(self, addon, useShortFormat=True, isChildComment=False):
        title = self.__getAddonTitleStr(addon)
        desc  = self.__getAddonDescriptionStr(addon, useShortFormat)[0]
        msg = "{0} :: {1}".format(title, desc)
        if isChildComment:
            msg = "{0}{0}{1}".format(Helper.INDENT, msg)
        return [msg,]
    

    def __getAddonTitleStr(self, addon):
        try:
            title = addon.title
        except AttributeError:
            title = addon.__class__.__name__
        return title.lower()
    

    def __getAddonDescriptionStr(self, addon, useShortFormat=True):
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
    
    
    def __getAllAddonDescriptions(self, useShortFormat=True):
        addons = ircBot.addonList[:]
        help_messages = Helper.HELP_ADDONS
        for addon in addons:
            help_messages.extend(self.__getAddonIntro(addon, useShortFormat, True))
        return help_messages
    
    ### command help extracty functions
    

    def __getCommandHelpFromAddon(self, addon, command, useShortFormat=True, isChildComment=False):
        # assumes already tested that cmd in addon.commandList
        desc_list = None
        try:
            desc_list = addon.helpList[command]
        except (AttributeError, KeyError):
            return self.__makeCommandNoneMessage(command, useShortFormat, isChildComment)
        msg = "{0}{1} :: {2}".format(Helper.PREFIX, command, desc_list[0])
        if isChildComment:
            msg = Helper.INDENT + msg
        help_messages = [msg,]
        if len(desc_list) > 1:
            for i in range(1,len(desc_list)):
                help_messages.append("{0}{0}{1}".format(Helper.INDENT, desc_list[i]))
        return [msg,]
    

    def __getAllCommandsHelpFromAddon(self, addon, useShortFormat=True):
        help_messages = []
        for command in addon.commandList:
            try:
                help_messages.extend(self.__getCommandHelpFromAddon(addon, command, useShortFormat, True))
            except:
                help_messages.extend((self.__makeCommandNoneMessage(command, useShortFormat, True),))
        return help_messages
    
    
    
    ### formatting functions
    

    def __makeCommandNoneMessage(self, command, useShortFormat=True, isChildComment=True):
        msg = "{0}{1} :: {2}"
        if isChildComment:
            msg = Helper.INDENT + msg
        if useShortFormat:
            return [msg.format(Helper.PREFIX, command, Helper.NONE_CMD_SHORT[0]),]
        else:
            return [msg.format(Helper.PREFIX, command, Helper.NONE_CMD_LONG[0]),]
    

    def __makeInvokeCommand(self, command, useShortFormat=True, **args):
        if useShortFormat:
            msg = "Read more:"
        else:
            msg = "For a more in depth explanation use:"
        cmdToInvoke = "{0}{1}".format(Helper.PREFIX, command)
        if args:
            for arg in args:
                cmdToInvoke = "{0} {1}".format(cmdToInvoke, arg)
        return "{0} {1}".format(msg, cmdToInvoke)
    
    
    ### speak functions:
    

    def __sayToChannel(self, help_messages, **channels):
        ##TODO write handling for multi-channel
        for message in help_messages:
            ircHelpers.sayInChannel(message)
    

    def __sayToUser(self, user, help_messages):
        for message in help_messages:
            ircHelpers.pmInChannel(user, message)
    

    def __sayDefaultToUser(self, user, useShortFormat=True):
        if useShortFormat:
            self.__sayToUser(user, Helper.HELP_ROOT)
        else:
            self.__sayToUser(user, Helper.HELP_VERBOSE)
    
    def __sayDefaultToChannel(self, useShortFormat=True):
        if useShortFormat:
            self.__sayToChannel(Helper.HELP_ROOT)
        else:
            self.__sayToChannel(Helper.HELP_VERBOSE)
            