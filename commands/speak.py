def create(commands):
    commands['say'] = speak

def speak(ircHelper, arguments):
    ircHelper.send('PRIVMSG %s :%s\r\n' % (ircHelper.channel, arguments))
