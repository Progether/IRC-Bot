from core import ircBot

import re

@ircBot.registerBehaviour()
class Hello:
    def __init__(self):
        self.regex = re.compile(r":(?P<user>\w+)!~.+!!log")

    def perform(self, data):
        match = self.regex.match(data)
        if match:
            ircBot.cLog.playLog()
 
