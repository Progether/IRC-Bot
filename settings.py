from configparser import ConfigParser
import os

current_directory = os.getcwd()
FILE_NAME = "%s/settings.txt" % current_directory

# default settings (and template for generated file contents)
file_raw = """  [settings]
                
                ## bot user:
                nick     = progether
                password = progether_bot
                
                ## channel:
                channel  = #reddit-progether
                network  = irc.freenode.net
                port     = 6667
                
                ## database
                db_name = d2k2tmq3q2lk62
                db_user = ddvzstnjeyvtkk
                db_pass = qiJbYxnbFTlXBAtRiyRkXGkFub
                db_host = ec2-23-23-80-55.compute-1.amazonaws.com
                db_port = 5432
                
                ## bot commands
                quit        = !!quit
                bot_command = !!
                """

def create_config():
    config_file = open(FILE_NAME, 'w')
    
    file_content = file_raw.splitlines()
    for line in file_content:
        config_file.write(line.strip() + "\n")
    config_file.close()

def read_config():
    config = dict()
    config_file = ConfigParser()
    created_new_file = False
    while True:
        try:
            config_file.read_file(FILE_NAME)        # attempt to open existing file
            break
        except (IOError, FileNotFoundError) as e:
            print(e)
            if not created_new_file:
                create_config()                     # try to create file if not exists
            else:
                config_file.read_raw(file_raw)      # else read direct from default string
                break

    
    config['nick']     = config_file.get('settings', 'nick')
    config['password'] = config_file.get('settings', 'password')
    config['channel']  = config_file.get('settings', 'channel')
    config['network']  = config_file.get('settings', 'network')
    config['port']     = config_file.get('settings', 'port')
    
    config['db_name'] = config_file.get('settings', 'db_name')
    config['db_user'] = config_file.get('settings', 'db_user')
    config['db_pass'] = config_file.get('settings', 'db_pass')
    config['db_host'] = config_file.get('settings', 'db_host')
    config['db_port'] = config_file.get('settings', 'db_port')
    
    config['quit']        = config_file.get('settings', 'quit')
    config['bot_command'] = config_file.get('settings', 'bot_command')
    return config


if __name__ == '__main__':
    create_config()
    conf = read_config()
    print(conf['nick'])
    print(conf['network'])
    print(conf['port'])
    print(conf['channel'])
    print(conf['password'])
