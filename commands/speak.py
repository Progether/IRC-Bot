#example of how to make commands
#make another file in this directory called something.py



from commandModule import command #import the command decorator
@command('say') #decorate a function with it, and supply the command you want it to be triggerd by. for example this one will be triggered when someone says !!say something
def speak(ircHelper, arguments):#the function takes an irchelper and arguments
    ircHelper.send('PRIVMSG %s :%s\r\n' % (ircHelper.channel, arguments)) #arguments are what comes after the command, for example !say hello, hello witll be the argument
    #irchelper is how you interact with the irc, it has functions and vars that can be used
