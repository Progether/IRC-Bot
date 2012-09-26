import re

class CommandModule:
    def __init__(self):
        self.regexSplitCommand = re.compile(r"!!(?P<command>\w+)\s(?P<arguments>.*).*")
        
    def runCommand(self, command):
        split = self.regexSplitCommand.match(command)
        commandName = split.group('command')
        commandArguments = split.group('arguments')
        print commandName + "---" + commandArguments
