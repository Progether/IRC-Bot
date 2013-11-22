class ConfigParser:
    def __init__(self):
        self.config = dict()

    def read(self, lines):
        
        for line in lines:
            item = line.strip()
            if '[settings]' in item:
                self.config = { "settings" : dict() }       
            elif '=' in item:
                items = item.split("=")
                key = items[0].strip()
                try:
                    value = items[1].split()[0].strip()
                    if value.startswith('#'):
                        value = ''
                except (IndexError):
                    value = ''
                self.config['settings'][key] = value
            else:
                pass
            
                

    def read_file(self, settings_file):
        with open(settings_file) as f:
            lines = f.readlines()
            self.read(lines)
            f.close()
            
    def read_raw(self, raw_text):
        lines = raw_text.splitlines()
        self.read(lines)
            

    def get(self, first_key, second_key):
        value = self.config[first_key][second_key]
        return value
