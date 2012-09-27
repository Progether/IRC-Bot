class IRCHelper:
    def __init__(self, ircbot):
        self.ircbot = ircbot

        self.network = self.ircbot.network
        self.port = self.ircbot.port
        self.channel = self.ircbot.channel
        self.nickname = self.ircbot.nickname

    def send(self, thingToSend):
        self.ircbot.socket.send(thingToSend)
