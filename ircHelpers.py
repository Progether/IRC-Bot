from core import ircBot

def getNetwork():
    return ircBot.network

def getPort():
    return ircBot.port

def getChannel():
    return ircBot.channel

def getNick():
    return ircBot.nickname

def send(thingToSend):
    ircBot.socket.send(thingToSend)


