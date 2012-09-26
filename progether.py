#Need to read/write a config file
def create_config(file_name):
    config_file = open(file_name, 'w')
    file_content = """\
nick = progether-irc
host = example
port = 6667
channels = ['#progether']
    """
    config_file.write(file_content)
    config_file.close()
    
if __name__ == '__main__':
    create_config("test.txt")
