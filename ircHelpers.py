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

def sayInChannel(thingToSay):
    send('PRIVMSG %s :%s\r\n' % (getChannel(), thingToSay))

def privateMessage(user, message):
    send('PRIVMSG %s :%s\r\n' % (user, message))

def callForUsers():
    send('NAMES %s\r\n' % getChannel())