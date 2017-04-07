import os
from system_info import default_native_dot_minecraft_directory

dot_minecraft_directory = None

if os.path.exists(default_native_dot_minecraft_directory):
    os.chdir(default_native_dot_minecraft_directory)
    dot_minecraft_directory = default_native_dot_minecraft_directory
elif os.path.exists('.minecraft'):
    os.chdir('.minecraft')
    dot_minecraft_directory = os.getcwd()
elif os.path.exists('../minecraft'):
    os.chdir('../minecraft')
    dot_minecraft_directory = os.getcwd()
