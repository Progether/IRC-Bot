from configparser import ConfigParser
import os

current_directory = os.getcwd()
FILE_NAME = "%s/settings.txt" % current_directory

# default settings (and template for generated 'settings.txt file contents)
file_raw = """  [settings]

                ## bot user:
                nick     = progether
                password = progether_bot

                ## channel:
                channel  = reddit-progether
                network  = irc.freenode.net
                port     = 6667

                ## database:
                db_name = d2k2tmq3q2lk62
                db_user = ddvzstnjeyvtkk
                db_pass = qiJbYxnbFTlXBAtRiyRkXGkFub
                db_host = ec2-23-23-80-55.compute-1.amazonaws.com
                db_port = 5432

                ## bot settings
                command_prefix    = !!
                quit              = !!quit      # depreciated
                logAllToConsole   = False        # True or False
                respondToNotFound = False        # True or False
                """

def create_config():
    print(".. Attempting to create new configuration file..")
    try:
        config_file = open(FILE_NAME, 'w')

        file_content = file_raw.splitlines()
        for line in file_content:
            config_file.write(line.strip() + "\n")
        print (".. Success")
    except IOError:
        print("!! Could not create new settings.txt configuration file")
    finally:
        try:
            config_file.close()
        except Exception:
            pass

def read_config():
    config = dict()
    config_file = ConfigParser()
    created_new_file = False
    while True:     # loop until we have either a file to read or failing that the default string to use
        try:
            config_file.read_file(FILE_NAME)        # attempt to open existing file
            break                                   # exit loop if not fails
        except (FileNotFoundError):
            print("!! settings.txt configuration file not found")
        except (IOError):
            print("!! error reading settings.txt configuration file")
        if not created_new_file:
            create_config()                     # try to create file if not exists
        else:
            config_file.read_raw(file_raw)      # else read direct from default string
            break

    try:
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

        config['command_prefix']    = config_file.get('settings', 'command_prefix')
        config['quit']              = config_file.get('settings', 'quit')
        config['logAllToConsole']   = config_file.get('settings', 'logAllToConsole')
        config['respondToNotFound'] = config_file.get('settings', 'respondToNotFound')
        return config
    except Exception as e:
        import sys
        print("!! Failed to retrieve all required settings. Perhaps you need to regenerate your settings.txt")
        print("!! Quitting with error:")
        print(e)
        sys.exit()



if __name__ == '__main__':
    create_config()
    conf = read_config()
    print("=== irc server ===")
    print("nick: " +conf['nick'])
    print("pass: " +conf['password'])
    print("chan: " +conf['channel'])
    print("netw: " +conf['network'])
    print("port: " +conf['port'])

    print("=== database ==")
    print("db_name: " +conf['db_name'])
    print("db_user: " +conf['db_user'])
    print("db_pass: " +conf['db_pass'])
    print("db_host: " +conf['db_host'])
    print("db_port: " +conf['db_port'])

    print("=== bot settings ===")
    print("cmd_pref: " +conf['command_prefix'])
    print("cmd_quit: " +conf['quit'])
    print("logAll:   " +(str) (conf['logAllToConsole']   == 'True'))
    print("respond:  " +(str) (conf['respondToNotFound'] == 'True'))
