from core import ircBot, AddonBase
import ircHelpers
import re
import requests
import json
import string

@ircBot.registerAddon()
class LinkHelp(AddonBase):
    def __init__(self):
        self.commandList = {}
        self.messageList = [self.parse_for_links]


    def parse_for_links(self, messageInfo):
        message = messageInfo['message'].replace('\r', '')
        if "/r/" in message:
            self.respond_with_subreddit(message)

    def respond_with_subreddit(self, message):
        potential_reddits = re.compile("(/r/\S+)").findall(message)
        reddits=[]
        for reddit in potential_reddits:
            reddit = reddit.rstrip(string.punctuation)
            resp = requests.get("http://www.reddit.com"+reddit+"/about.json", headers={ 'User-Agent' : '/r/progether bot' })
            try:
                data = resp.json()
                if not 'error' in data:
                    reddits.append("http://www.reddit.com"+reddit)
                else:
                    reddits.append("The subreddit "+reddit+" doesn't exist")
            except:
                reddits.append("The subreddit "+reddit+" doesn't exist")
        ircHelpers.sayInChannel(', '.join(reddits))
