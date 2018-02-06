"""
System infomation and useful directories storage.
"""
import platform
import os
import shutil
import sys
import logging

if getattr(sys, 'frozen', False):
    launcher_dir = os.path.dirname(sys.executable)
else:
    launcher_dir = sys.path[0]

system = {
    'Windows': 'windows', 'Darwin': 'osx', 'Linux': 'linux'}[platform.system()]

arch = {'64bit': '64', '32bit': '32'}[platform.architecture()[0]]

version = platform.version()

java_dir = shutil.which('javaw')
# if default_java_dir and os.path.islink(default_java_dir):
#     default_java_dir = os.readlink(default_java_dir)

# set default minecraft directory
# detects the following:
# 1. Mojang-preferred dir
# 2. launcher dir
# 3. the parent folder of launcher dir
if system == 'windows':
    system_minecraft_dir = os.path.join(os.getenv('APPDATA'), '.minecraft')
elif system == 'osx':
    system_minecraft_dir = os.path.expanduser("~/Library/Application Support/minecraft")
else:
    system_minecraft_dir = os.path.expanduser("~/.minecraft")
if os.path.exists(system_minecraft_dir):
    minecraft_dir = system_minecraft_dir
elif os.path.exists(os.path.join(launcher_dir, '.minecraft')):
    minecraft_dir = os.path.join(launcher_dir, '.minecraft')
if not os.path.exists(minecraft_dir):
    minecraft_dir = os.path.join(launcher_dir, '.minecraft')
    if not os.path.exists(minecraft_dir):
        minecraft_dir = os.path.join(os.path.dirname(launcher_dir), '.minecraft')
        if not os.path.exists(minecraft_dir):
            minecraft_dir = None


def build_minecraft_directories():
    global launcherprofiles, launcherprofiles_backup, libraries, assets
    launcherprofiles = os.path.join(
        minecraft_dir, 'launcher_profiles.json')
    launcherprofiles_backup = os.path.join(
        minecraft_dir, 'launcher_profiles.json.millibackup')
    libraries = os.path.join(minecraft_dir, 'libraries')
    assets = os.path.join(minecraft_dir, 'assets')


def build_launcher_directories():
    global config, log
    config = os.path.join(launcher_dir, 'millilauncher.ini')
    log = os.path.join(launcher_dir, 'millilauncher.log')
    logging.basicConfig(filename=log, filemode='w', level=logging.DEBUG)


build_launcher_directories()
if minecraft_dir is not None:
    build_minecraft_directories()
