# Just displays the reddit link for Progether

from commandModule import command

@command('wiki')
def speak(ircHelper, arguments):
    ircHelper.send('PRIVMSG %s :%s\r\n' % (ircHelper.channel, "http://http://progether.wikia.com/wiki/Progether_Wiki/"))
