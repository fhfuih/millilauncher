"""
Configuration settings and storage.
"""
from sys import path as syspath
import os.path
import json
from collections import OrderedDict

from api import systeminfo as _info

_config_file = os.path.join(syspath[0], 'millilauncher.json')

_default = OrderedDict(
    exit_on_launch=False,
    fullscreen=False,
    javaw_dir=_info.default_java_directory,
    max_mem=2048,
    mc_dir=_info.default_minecraft_directory,
    username='Steve'
)

class _Config(OrderedDict):
    def __init__(self):
        super().__init__()
        try:
            with open(_config_file) as fp:
                obj = json.load(fp)
                self.update(json.load(fp, object_pairs_hook=OrderedDict))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.__dict__['first_launch'] = True
            self.reset()
        else:
            self.__dict__['first_launch'] = False
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

config = None

if config is None:
    config = _Config()
