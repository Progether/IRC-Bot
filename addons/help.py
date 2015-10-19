from core import ircBot, AddonBase
import ircHelpers

@ircBot.registerAddon()
class Helper(AddonBase):

    '''
      Set help messages for commands within their own classes. Refer to 'mail.py' for an example of how to properly implement it. All messages must be lists of Strings. Each separate String will get printed on a new line when passed to user/channel. If no help is found for a command argument (either no command exists or no help found) applicable 'HELP_NONE_' variant is selected.
    '''
    # static strings
    PREFIX = ircBot.command_prefix  # to construct command examples
    INDENT = "  "                   # for formatting the output

    # required descriptions for help addon
    help_description = ["Get help on the bot's functionality",]
    help_help     = ["{0}help [addon/command] :: Get help on bot's commands.'".format(PREFIX),]
    help_aid = ["{0}aid [user] [help arguments] :: Send help to another user. Usage is the same as for {0}help.".format(PREFIX),]


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
            help_messages = self.__getCommandHelpFromAddon(self.title, 'aid', False)
            ircHelpers.privateMessage(requesting_user, *help_messages)
        else:
            ##TODO Perform test for user online and known to bot
            target_user = args.pop(0)
            self.__giveHelp(target_user, args)

    ### function that does the heavy lifting. can be called recursively for changing target of the help (or other)
    def __giveHelp(self, user, split_arguments, times_run=0):
        if times_run > 5:
            print("!! Too many recursive calls to Help.__giveHelp(). Giving up.")
            return

        num_args = len(split_arguments)

        # bare 'help' command on its own
        if num_args == 0:
            if self.debug: print("== No args, giving default")
            help_message = ["Welcome to progether! There may not always be a lot of activity here, just stick around. IRC use requires some patience. All commands for the bots can also be done by private messages: /msg {0} {1}[command] [**args]. For information about IRC read https://irchelp.org/irchelp/new2irc.html".format(ircBot.nickname, Helper.PREFIX),
                    "{0}The format is: {1}help ['commands'/'addons'/commandName/addonName] For more information on useage checkout https://github.com/Progether/IRC-Bot/blob/master/README.md".format(Helper.INDENT, Helper.PREFIX),]
            ircHelpers.privateMessage(user, *help_message)

        # has arguments we need to parse
        else:
            first_arg = split_arguments[0].lower()

            # display all help at once:
            if first_arg in ('all', 'a'):
                if self.debug: print("== Found CASE_ALL")
                help_messages = self.__getAllHelp()
                ircHelpers.privateMessage(user, *help_messages)

            # list all addon packages and descriptions
            elif first_arg in ('addons', 'add'):
                if self.debug: print("== Found CASE_ADDONS")
                help_messages = self.__getAllAddonDescriptions()
                ircHelpers.privateMessage(user, *help_messages)

            # list all commands available in short form (for recap):
            elif first_arg in ('commands', 'cmds'):
                if self.debug: print("== Found CASE_CMDS")
                help_messages = self.__getAllCompactAddonHelp()
                ircHelpers.privateMessage(user, *help_messages)

            # otherwise parse argument as a command
            else:
                if self.debug: print("== No mods left. Parse cmd: " +split_arguments[0])
                help_messages = self.__getHelpForSingleCmd(split_arguments[0])
                ircHelpers.privateMessage(user, *help_messages)


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
                    return self.__getFullAddonHelp(addon)
            except (AttributeError) as e:
                if self.debug: print("== AttrError in getHelpOnSingleCmd() - title\r\n", e.args[0])
            try:
                if command in addon.commandList.keys():
                    if self.debug: print("== Found cmd in addonList keys: %s" % self.__getAddonTitleStr(addon))
                    return self.__getCommandHelpFromAddon(addon, command, False)
            except (AttributeError, KeyError) as e:
                if self.debug: print("== Attr/KeyError in getHelpOnSingleCmd() - cmdList\r\n", e.args[0])
        if self.debug: print("== serving default cmd missing")
        return self.__makeCommandNoneMessage(command)

    def __getAllHelp(self):
        help_messages = ["Welcome to progether, a collection of programmers teaching each other how not to do things.",
                "{0}Here's what this bot can do:".format(Helper.INDENT) ]
        addons = ircBot.addonList[:]
        for addon in addons:
            help_messages.extend(self.__getFullAddonHelp(addon))
        return help_messages

    def __getFullAddonHelp(self, addon):
        help_messages = self.__getAddonIntro(addon)
        help_messages.extend(self.__getAllCommandsHelpFromAddon(addon))
        return help_messages

    def __getAllCompactAddonHelp(self):
        help_messages = []
        addons = ircBot.addonList[:]
        for addon in addons:
            help_messages.extend(self.__getCompactAddonHelp(addon))
        return help_messages

    def __getCompactAddonHelp(self, addon):
        help_messages = self.__getAddonIntro(addon)
        cmds_summary = "{}Available commands: ".format(Helper.INDENT)
        try:
            for cmd in addon.commandList:
                cmds_summary = "{0}, {1}".format(cmds_summary, "{0}{1}, ".format(Helper.PREFIX, cmd)).rstrip(', ')
        except (AttributeError):
            if self.debug: print("== AttrErr in getCompactAddonHelp")
        help_messages.extend((cmds_summary[2:],))
        return help_messages


    ### addon info extract functions
    def __getAddonIntro(self, addon, isChildComment=False):
        title = self.__getAddonTitleStr(addon)
        desc  = self.__getAddonDescriptionStr(addon)[0]
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

    def __getAddonDescriptionStr(self, addon):
        desc = None
        try:
            desc = addon.help_description
        except AttributeError:
            desc = ["No description found"]
        return desc

    def __getAllAddonDescriptions(self):
        addons = ircBot.addonList[:]
        help_messages = HELP_ADDONS = ["These are the currently active addon packages. For details of the commands within any of them try:",
                "{0}Addon explore command: {1}help [addon_title]".format(Helper.INDENT, Helper.PREFIX)]
        for addon in addons:
            help_messages.extend(self.__getAddonIntro(addon))
        return help_messages


    ### command help extract functions
    def __getCommandHelpFromAddon(self, addon, command, isChildComment=False):
        # assumes already tested that cmd in addon.commandList
        desc_list=[]
        try:
            desc_list = addon.helpList[command]
        except (AttributeError, KeyError):
            return self.__makeCommandNoneMessage(command, isChildComment)
        msg = "{0}{1} :: {2}".format(Helper.PREFIX, command, desc_list[0])
        if isChildComment:
            msg = Helper.INDENT + msg
        help_messages = [msg,]
        if len(desc_list) > 1:
            for i in range(1,len(desc_list)):
                help_messages.append("{0}{0}{1}".format(Helper.INDENT, desc_list[i]))
        return [msg,]

    def __getAllCommandsHelpFromAddon(self, addon):
        help_messages = []
        for command in addon.commandList:
            try:
                help_messages.extend(self.__getCommandHelpFromAddon(addon, command, True))
            except:
                help_messages.extend((self.__makeCommandNoneMessage(command, True),))
        return help_messages


    ### formatting functions
    def __makeCommandNoneMessage(self, command, isChildComment=True):
        msg = "{0}{1} :: {2}"
        if isChildComment:
            msg = Helper.INDENT + msg
        return [msg.format(Helper.PREFIX, command, "No help found.")]

    def __makeInvokeCommand(self, command, **args):
        msg = "Read more:"
        cmdToInvoke = "{0}{1}".format(Helper.PREFIX, command)
        if args:
            for arg in args:
                cmdToInvoke = "{0} {1}".format(cmdToInvoke, arg)
        return "{0} {1}".format(msg, cmdToInvoke)
