import os
import logging
import configparser

import dirs

_config = configparser.ConfigParser()
_config.optionxform = lambda x: x

_default = {
    "DEFAULT": {
        "ExitOnLaunch": 'yes',
        "JavaDir": dirs.java_dir,
        "MinecraftDir": dirs.minecraft_dir,
        "FirstRun": not os.path.exists(dirs.config),
        "LoginMode": "offline",
        "Username": "Steve",
        "Fullscreen": 'no',
        "MaxMemory": 2048,
    }
    # "LAUNCHER": {
    #     "ExitOnLaunch": 'yes',
    #     "JavaDir": dirs.java_dir,
    #     "MinecraftDir": dirs.minecraft_dir,
    #     "FirstRun": not os.path.exists(dirs.config),
    # },
    # "AUTHENTICATION": {
    #     "LoginMode": "offline",
    #     "Username": "Steve",
    # },
    # "GAMING": {
    #     "Fullscreen": 'no',
    #     "MaxMemory": 2048,
    # },
}

_config.read_dict(_default)
if not os.path.exists(dirs.config):
    logging.info("Config file not found or corrupted. Default values used.")
else:
    _config.read(dirs.config)
logging.info('Config file is stored in %s', dirs.config)

config = _config['DEFAULT']

def save():
    with open(dirs.config, 'w') as fp:
        _config.write(fp)


def reset():
    _config.read_dict(_default)
    config['FirstRun'] = 'yes'
