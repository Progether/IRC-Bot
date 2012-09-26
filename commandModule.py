import re

commandList = dict()
def command(commandName, **options):
        def decorator(f):
            commandList[commandName] = f
            return f
        return decorator

from commands import * 

class CommandModule:
    def __init__(self, ircHelper):
        self.regexSplitCommand = re.compile(r"!!(?P<command>\w+)\s(?P<arguments>.*).*")

        self.ircHelper = ircHelper
        
    def runCommand(self, command):
        split = self.regexSplitCommand.match(command)
        if split:
            commandName = split.group('command')
            commandArguments = split.group('arguments')
            if commandList.has_key(commandName):
                commandList[commandName](self.ircHelper, commandArguments)
            print commandName + "---" + commandArguments
