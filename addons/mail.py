from core import ircBot, AddonBase
import ircHelpers

import re

@ircBot.registerAddon()
class Mail(AddonBase):
    def __init__(self):
	   self.commandList = {"mail" : self.mail, "mymail" : self.myMail}
	   self.joinList = [self.notify]

           self.regexMail = re.compile(r"(?P<user>\w+)\s(?P<message>.+)")

	   self.mailDict = dict()

    def myMail(self, arguments, messageInfo):
        if self.mailDict.has_key(messageInfo['user']):
            for mail in self.mailDict[messageInfo['user']]:
                ircHelpers.privateMessage(messageInfo['user'], mail)
            self.mailDict[messageInfo['user']] = list()

    def mail(self, arguments, messageInfo):
        regex = self.regexMail.match(arguments)
        if regex:
            if not self.mailDict.has_key(regex.group('user')):
                self.mailDict[regex.group('user')] = list()
            self.mailDict[regex.group('user')].append(messageInfo['user'] + ': ' + regex.group('message'))

    def notify(self, user):
        if self.mailDict.has_key(user):
            if len(self.mailDict[user]) > 0:
                ircHelpers.privateMessage(user, 'you have mail, !!mymail to view')
