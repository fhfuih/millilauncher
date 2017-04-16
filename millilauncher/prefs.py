import json

class Prefs(object):
    def __init__(self, file='./millilauncher.json'):
        self.file = file
        try:
            with open(file) as fp:
                self.__dict__.update(json.load(fp))
        except FileNotFoundError:
            self.mc_dir = None
            self.java_dir = None
            self.max_mem = None
            self.username = None
            self.fullscreen = False
            self.exit_on_launch = False

    def save(self):
        with open(self.file, 'w') as fp:
            json.dump(self.__dict__, fp, ensure_ascii=False, indent=4)
