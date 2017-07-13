"""
Configuration settings and storage.
"""
import json
import logging
import os
import sys

from .clientcore.systeminfo import (default_java_directory,
                                    default_minecraft_directory, launcher_dir)

_config_file = os.path.join(launcher_dir, 'millilauncher.json')

_logging_file = os.path.join(launcher_dir, 'millilauncher.log')

logging.basicConfig(filename=_logging_file, filemode='w', level=logging.DEBUG)

_default = {
    # download_source:'Mojang',
    "exit_on_launch": False,
    "fullscreen": False,
    "java_dir": default_java_directory,
    # login_mode:'Offline',
    "max_mem": 2048,
    "mc_dir": default_minecraft_directory,
    "username": "Steve"
}

class _Config(dict):
    def __init__(self):
        super().__init__()
        try:
            with open(_config_file) as fp:
                self.update(json.load(fp))
        except FileNotFoundError:
            logging.info('Config file not found.')
            self.__dict__['first_run'] = True
            self.reset()
        except json.decoder.JSONDecodeError:
            logging.warning('Config file is corrupted.')
            self.__dict__['first_run'] = True
            self.reset()
        else:
            self.__dict__['first_run'] = False
            self._confirm()
        finally:
            logging.info('Config file is stored in %s', _config_file)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, val):
        self[key] = val

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
