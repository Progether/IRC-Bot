class IRCHelper:
    def __init__(self, ircbot):
        self.ircbot = ircbot

        self.channel = self.ircbot.channel

    def send(thingToSend):
        self.ircbot.socket.send(thingToSend)
        
