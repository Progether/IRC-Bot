from core import ircBot
import ircHelpers

import re

@ircBot.registerBehaviour()
class Hello:
    def __init__(self):
	self.regex = re.compile(r":(?P<user>\w+)!~.+\sJOIN\s") 

    def perform(self, data):
	match = self.regex.match(data)
        if match:
	    ircHelpers.sayInChannel('Hello %s!' % match.group('user'))
 
