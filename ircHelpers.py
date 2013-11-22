from core import ircBot

debug = False

def getNetwork():
    return ircBot.network

def getPort():
    return ircBot.port

def getChannel():
    return ircBot.channel

def getNick():
    return ircBot.nickname

def send(thingToSend):
    if debug: print("<< %s" % thingToSend)
    ircBot.socket.send(thingToSend)

def sayInChannel(thingToSay):
    string = 'PRIVMSG %s :%s\r\n' % (getChannel(), thingToSay)
    send(string.encode("UTF-8"))

def privateMessage(user, message):
    string = 'PRIVMSG %s :%s\r\n' % (user, message)
    send(string.encode("UTF-8"))
    
def pmInChannel(user, message):
    string = 'NOTICE %s :%s\r\n' % (user, message)
    send(string.encode("UTF-8"))

def callForUsers():
    send('NAMES %s\r\n' % getChannel())

def changeNick(newNick):
    string = 'NICK %s' % newNick
    send(string.encode("UTF-8"))
