import re

class CommandModule:
    def __init__(self):
        self.commandList = dict()
        self.regexSplitCommand = re.compile(r"!!(?P<command>\w+)\s(?P<arguments>.*).*")

    def runCommand(self, command, messageInfo):
        split = self.regexSplitCommand.match(command)
        if split:
            commandName = split.group('command')
            commandArguments = split.group('arguments')
            if self.commandList.has_key(commandName):
                self.commandList[commandName].onRun(commandArguments, messageInfo)

