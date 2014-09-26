from core import IRCBot
from addons import *
import yaml

def main():
    """
    Imports settings and starts the bot.
    """
    # Attempt to open and read the settings file
    try:
        with open("irc.yaml", 'r') as settings_file:
            conf = yaml.load(settings_file)
    except FileNotFoundError:
        print("Config file not found. Make sure irc.yaml exists in this directory.")
        exit(1)

    # Print the configuration settings
    print("=== irc server ===")
    print("nick: " + conf['user']['nick'])
    print("pass: " + conf['user']['password'])
    print("chan: " + conf['channel']['name'])
    print("netw: " + conf['channel']['network'])
    print("port: " + conf['channel']['port'])

    print("=== database ==")
    print("db_name: " + conf['database']['name'])
    print("db_user: " + conf['database']['user'])
    print("db_pass: " + conf['database']['pass'])
    print("db_host: " + conf['database']['host'])
    print("db_port: " + conf['database']['port'])

    print("=== bot settings ===")
    print("cmd_pref: " + conf['settings']['prefix'])
    print("logAll:   " + str(conf['settings']['logAllToConsole']))
    print("respond:  " + str(conf['settings']['respondToNotFound']))

    # Attempt to create an IRCBot object
    bot = IRCBot(conf)

    # If that succeeded, start the bot
    bot.run()

if __name__ == '__main__':
    main()