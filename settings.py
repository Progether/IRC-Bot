from ConfigParser import ConfigParser

def create_config():
    config_file = open("settings.txt", 'w')
    file_content = """\
                    [settings]
                    nick = tmpircbotname
                    port = 6667
                    network = irc.freenode.net
                    channel = ##ProgetherBotTest
                    password = 1234test
                    """
    file_content = file_content.splitlines()
    for line in file_content:
        config_file.write(line.strip() + "\n")
    config_file.close()

def read_config():
    config = dict()
    config_file = ConfigParser()
    config_file.read("settings.txt")
    config['nick'] = config_file.get('settings', 'nick')
    config['network'] = config_file.get('settings', 'network')
    config['port'] = config_file.get('settings', 'port')
    config['channel'] = config_file.get('settings', 'channel')
    config['password'] = config_file.get('settings', 'password')
    return config
    
    
    
if __name__ == '__main__':
    create_config()
    conf = read_config()
    print conf['nick']
    print conf['network']
    print conf['port']
    print conf['channel']
    print conf['password']
