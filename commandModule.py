import re

class CommandModule:
    def __init__(self, ircHelper):
        self.commandList = dict()

        self.ircHelper = ircHelper

        self.regexSplitCommand = re.compile(r"!!(?P<command>\w+)\s(?P<arguments>.*).*")

    def runCommand(self, command):
        split = self.regexSplitCommand.match(command)
        if split:
            commandName = split.group('command')
            commandArguments = split.group('arguments')
            if self.commandList.has_key(commandName):
                self.commandList[commandName].onRun(commandArguments)

