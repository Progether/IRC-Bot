# Just displays the reddit link for Progether

from commandModule import command

@command('reddit')
def speak(ircHelper, arguments):
    ircHelper.send('PRIVMSG %s :%s\r\n' % (ircHelper.channel, "http://reddit.com/r/progether/"))
