import platform as pf
import os
import shutil

def _get_default_minecraft_directory():
    'Attempt to detect .minecraft folder. Returns None if failed.'
    if system == 'windows':
        native_directory = os.path.join(os.getenv('APPDATA'), '.minecraft')
    elif system == 'osx':
        native_directory = os.path.join(os.getenv('HOME'), 'Library',
                                        'Application Support', '.minecraft')
    else:
        native_directory = os.path.join(os.getenv('HOME'), '.minecraft')

    if os.path.exists(native_directory):
        return native_directory
    elif os.path.exists('.minecraft'):
        return os.path.abspath('.minecraft')
    elif os.path.exists('../minecraft'):
        return os.path.abspath('../minecraft')
    else:
        return None

system = {'Windows':'windows', 'Darwin':'osx', 'Linux':'linux'}[pf.system()]

architecture = {'64bit':'64', '32bit':'32'}[pf.architecture()[0]]

version = pf.version()

default_java_directory = shutil.which('javaw')
if default_java_directory and os.path.islink(default_java_directory):
    default_java_directory = os.readlink(default_java_directory)

default_minecraft_directory = _get_default_minecraft_directory()

if __name__ == '__main__':
    print(system, architecture, version)
    print(default_minecraft_directory)