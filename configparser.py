class ConfigParser:
    def __init__(self):
        self.config = dict()

    def read(self, FILE_Name):
        with open(FILE_Name) as f:
            content = f.readlines()
        for item in content:
            if "[settings]" in item:
                self.config = { "settings" : dict() }
            else:
                items = item.split("=")
                key = items[0].strip()
                value = items[1].strip()
                self.config['settings'][key] = value

    def get(self, first_key, second_key):
        value = self.config[first_key][second_key]
        return value
