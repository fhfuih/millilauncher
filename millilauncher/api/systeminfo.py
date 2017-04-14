import platform as pf
import os

system = {'Windows':'windows', 'Darwin':'osx', 'Linux':'linux'}[pf.system()]

architecture = pf.architecture()[0]

version = pf.version()

def get_default_minecraft_directory():
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

if __name__ == '__main__':
    print(system, architecture, version)
    print(get_default_minecraft_directory())