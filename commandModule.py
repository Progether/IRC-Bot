import re

import commands.speak

class CommandModule:
    def __init__(self, ircHelper):
        self.regexSplitCommand = re.compile(r"!!(?P<command>\w+)\s(?P<arguments>.*).*")
        self.commands = dict()

        self.ircHelper = ircHelper
        
        commands.speak.create(self.commands)
        
    def runCommand(self, command):
        split = self.regexSplitCommand.match(command)
        if split:
            commandName = split.group('command')
            commandArguments = split.group('arguments')
            if self.commands.has_key(commandName):
                self.commands[commandName](self.ircHelper, commandArguments)
            print commandName + "---" + commandArguments
