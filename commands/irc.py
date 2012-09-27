# Just displays the reddit link for Progether

from commandModule import command

@command('irc')
def speak(ircHelper, arguments):
    ircHelper.send('PRIVMSG %s :%s\r\n' % (ircHelper.channel, "server: irc.freenode.net, channel: #progether"))
