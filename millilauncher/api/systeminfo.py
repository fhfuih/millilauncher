"""
System infomation and useful directories storage.
"""
import platform as pf
import os
import shutil
import sys

launcher_dir = os.path.realpath(sys.path[0])

parent_dir = os.path.split(launcher_dir)[0]

def _get_default_minecraft_directory():
    """
    Attempt to detect .minecraft folder. Returns None if failed.
    """
    if system == 'windows':
        native_directory = os.path.join(os.getenv('APPDATA'), '.minecraft')
    elif system == 'osx':
        native_directory = os.path.expanduser("~/Library/Application Support/minecraft")
    else:
        native_directory = os.path.expanduser("~/.minecraft")

    if os.path.exists(native_directory):
        return native_directory
    path = os.path.join(launcher_dir, '.minecraft')
    if os.path.exists(path):
        return path
    path = os.path.join(parent_dir, '.minecraft')
    if os.path.exists(path):
        return path
    else:
        return None

system = {'Windows':'windows', 'Darwin':'osx', 'Linux':'linux'}[pf.system()]

architecture = {'64bit':'64', '32bit':'32'}[pf.architecture()[0]]

version = pf.version()

default_java_directory = shutil.which('javaw')
if default_java_directory and os.path.islink(default_java_directory):
    default_java_directory = os.readlink(default_java_directory)

default_minecraft_directory = _get_default_minecraft_directory()
