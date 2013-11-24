from core import ircBot
from queue import Queue
from threading import Thread
import time

debug = False

def getNetwork():
    return ircBot.network

def getPort():
    return ircBot.port

def getChannel():
    return ircBot.channel

def getNick():
    return ircBot.nickname

def flood_control():
    while True:
        item = ircBot.q.get()
        ircBot.socket.send(item)
        time.sleep(.8)
        ircBot.q.task_done()

def start_queue_thread():
    ircBot.q = Queue()
    thread = Thread(target=flood_control)
    thread.daemon = True
    thread.start()

def send(thingToSend):
    if debug: print("<< %s" % thingToSend)
    ircBot.q.put(thingToSend)

def sayInChannel(thingToSay):
    string = 'PRIVMSG %s :%s\r\n' % (getChannel(), thingToSay)
    send(string.encode("UTF-8"))

def privateMessage(user, *messages):
    for message in messages:
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
