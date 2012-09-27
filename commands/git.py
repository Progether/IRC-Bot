# Just displays the reddit link for Progether

from commandModule import command

@command('git')
def speak(ircHelper, arguments):
    ircHelper.send('PRIVMSG %s :%s\r\n' % (ircHelper.channel, "https://github.com/Progether"))
