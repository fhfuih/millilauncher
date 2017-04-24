import json
from sys import path
import os.path

from api import systeminfo as _info

_config_file = os.path.join(path[0], 'millilauncher.json') 

_default = {
    'minecraft_folder': _info.default_minecraft_directory,
    'javaw_file': _info.default_java_directory,
    'max_mem': 2048,
    'username': 'Steve',
    'fullscreen': False,
    'exit_on_launch': False
}

class _Config(dict):
    __slots__ = ()
    def __init__(self):
        super().__init__()
        try:
            with open(_config_file) as fp:
                self.update(json.load(fp))
        except FileNotFoundError:
            self.first_launch = True
            self.reset()
        else:
            self.first_launch = False
            self._confirm()

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        self[key] = val

    def save(self):
        with open(_config_file, 'w') as fp:
            json.dump(self, fp, ensure_ascii=False, indent=4)

    def reset(self):
        self.update(_default)
        self.save()

    def _confirm(self):
        for key, val in _default.items():
            self.setdefault(key, val)

config = _Config()

if __name__ == '__main__':
    if config.first_launch:
        print('first')
    else:
        config.username = 'Voila!'
        print('read!')
    config.save()
