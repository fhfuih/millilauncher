'''
Configuration values to be stored:
mcdir
javadir
maxmem
username
fullscreen
exitonlaunch
'''
from os import path
import json
from sys import argv
from configparser import ConfigParser
from api import systeminfo as _info

_config_file = path.join(argv[0], 'millilauncher.ini')

_defaults = {
    ('mc_dir', 'MinecraftFolderDirectory'): (_info.default_minecraft_directory, ''),
    ('java_dir', 'JavaExecutableDirectory'): (_info.default_java_directory, ''),
    ('max_mem', 'MaximumMemoryAllocated(MB)'): (2048, 'int'),
    ('username', 'Username'): ('Steve', 'int'),
    ('fullscreen', 'FullScreen'): (False, 'boolean'),
    ('exit_on_launch', 'ExitOnLaunch'): (False, 'boolean')
}


class _Config(object):
    def __init__(self):
        self._config = ConfigParser(defaults=_defaults)
        self.generated = not bool(self._config.read(_config_file)) # Is this config file generated or from a existing file.
        if self.generated:
            self._config.add_section('User')
            for (key, name), (value, typesuffix) in _defaults:
                self._config['DEFAULT'][name] = value
                setattr(key, property(self._getter(value, typesuffix), self._setter))

    def _getter(self, value, typesuffix):
        def _getter_core(self):
            val = value
            return getattr(self._config, 'get' + typesuffix)('User', val)
        return _getter_core

    def _setter(self, val):
        self._config.set('User', val)
