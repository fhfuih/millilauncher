import platform as pf
import os

system = {'Windows':'windows', 'Darwin':'osx', 'Linux':'linux'}[pf.system()]

architecture = pf.architecture()[0]

version = pf.version()

if system == 'windows':
    default_native_dot_minecraft_directory = os.path.join(os.getenv('APPDATA'), '.minecraft')
elif system == 'osx':
    default_native_dot_minecraft_directory = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', '.minecraft')
else:
    default_native_dot_minecraft_directory = os.path.join(os.getenv('HOME'), '.minecraft')

if __name__ == '__main__':
    print(system, architecture, version)
    print(default_native_dot_minecraft_directory)