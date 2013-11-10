from configparser import ConfigParser
import os

FILE_NAME = "settings.txt"

def create_config():
    config_file = open(FILE_NAME, 'w')
    file_content = """\
                    [settings]
                    nick = tmpircbotname
                    port = 6667
                    network = irc.freenode.net
                    quit = !!quit
                    channel = #reddit-progether
                    password = 1234test
                    """
    file_content = file_content.splitlines()
    for line in file_content:
        config_file.write(line.strip() + "\n")
    config_file.close()

def read_config():
    print(os.getcwd())
    config = dict()
    config_file = ConfigParser()
    try:
      with open(FILE_NAME):
        config_file.read(FILE_NAME)
    except IOError:
      create_config()
      config_file.read(FILE_NAME)
    config['nick'] = config_file.get('settings', 'nick')
    config['network'] = config_file.get('settings', 'network')
    config['port'] = config_file.get('settings', 'port')
    config['channel'] = config_file.get('settings', 'channel')
    config['quit'] = config_file.get('settings', 'quit')
    config['password'] = config_file.get('settings', 'password')
    return config


if __name__ == '__main__':
    create_config()
    conf = read_config()
    print(conf['nick'])
    print(conf['network'])
    print(conf['port'])
    print(conf['channel'])
    print(conf['password'])
