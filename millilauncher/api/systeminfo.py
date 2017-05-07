"""
System infomation and useful directories storage.
"""
import platform as pf
import os.path
import shutil
import sys

if getattr(sys, 'frozen', False):
    launcher_dir = os.path.dirname(sys.executable)
else:
    launcher_dir = sys.path[0]

system = {'Windows':'windows', 'Darwin':'osx', 'Linux':'linux'}[pf.system()]

architecture = {'64bit':'64', '32bit':'32'}[pf.architecture()[0]]

version = pf.version()

default_java_directory = shutil.which('javaw')
# if default_java_directory and os.path.islink(default_java_directory):
#     default_java_directory = os.readlink(default_java_directory)

if system == 'windows':
    default_minecraft_directory = os.path.join(os.getenv('APPDATA'), '.minecraft')
elif system == 'osx':
    default_minecraft_directory = os.path.expanduser("~/Library/Application Support/minecraft")
else:
    default_minecraft_directory = os.path.expanduser("~/.minecraft")
if not os.path.exists(default_minecraft_directory):
    default_minecraft_directory = os.path.join(launcher_dir, '.minecraft')
    if not os.path.exists(default_minecraft_directory):
        default_minecraft_directory = os.path.join(os.path.dirname(launcher_dir), '.minecraft')
        if not os.path.exists(default_minecraft_directory):
            default_minecraft_directory = None
