"""
Configuration settings and storage.
"""
from sys import path as syspath
import os.path
import json

from api import systeminfo as _info

_config_file = os.path.join(syspath[0], 'millilauncher.json')

_default = {
    # download_source:'Mojang',
    "exit_on_launch": False,
    "fullscreen": False,
    "java_dir": _info.default_java_directory,
    # login_mode:'Offline',
    "max_mem": 2048,
    "mc_dir": _info.default_minecraft_directory,
    "username": "Steve"
}

class _Config(dict):
    def __init__(self):
        super().__init__()
        try:
            with open(_config_file) as fp:
                obj = json.loads(fp.read())
                self.update(obj)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.__dict__['first_run'] = True
            self.reset()
        else:
            self.__dict__['first_run'] = False
            self._confirm()

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        self[key] = val

    # Why can't default __setitem__ work properly?
    # Which will clear all but the very key passed to it.
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def save(self):
        """
        Save the configuration file
        """
        with open(_config_file, 'w') as fp:
            json.dump(self, fp, ensure_ascii=False, indent=4, sort_keys=True)

    def reset(self):
        """
        Reset the configuration settings to default
        """
        self.update(_default)
        self.save()

    def _confirm(self):
        for key, val in _default.items():
            self.setdefault(key, val)

config = None

if config is None:
    config = _Config()
