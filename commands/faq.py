# Just displays the reddit link for Progether

from commandModule import command

@command('faq')
def speak(ircHelper, arguments):
    ircHelper.send('PRIVMSG %s :%s\r\n' % (ircHelper.channel, "http://code.reddit.com/wiki/help/faqs/progether"))
