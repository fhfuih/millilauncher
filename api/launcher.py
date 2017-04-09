import os
from zipfile import ZipFile
import version_dict as vd
import system_info as si

class Launcher(object):
    'Launcher Object'
    template_script = '{javaw} {extra} -Xmx{maxmem}M -Djava.library.path={native} -cp {libs} {main} {mcargs}'
    def __init__(self, mcdir, javadir='javaw'):
        self.mcdir = mcdir if mcdir else si.get_default_minecraft_directory()
        if not self.mcdir:
            raise FileNotFoundError('Invalid /.Minecraft/ directory.')
        os.chdir(self.mcdir)
        self.versions = vd.VersionsDict()

        self.extra_argument = '-Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true'

    # goal: launch(self, version_id, auth[tuple], server, size[tuple])
    def launch(self, version_id, username='Steve', maxmem=1024):
        'Launch Minecraft'
        version = self.versions.get(version_id)
        if not version:
            raise AttributeError('Version of this id does not exist.')
        jar = os.path.join(self.mcdir, 'versions', version.jar, version.jar + '.jar')
        libraries = ';'.join([lib.path for lib in version.libraries if lib.allow]) + ';' + jar
        mcargs = version.minecraft_arguments.format(auth_player_name=username,
                                                    version_name=version_id,
                                                    game_directory=self.mcdir,
                                                    assets_root=os.path.join(self.mcdir, 'assets'),
                                                    assets_index_name=version.assets,
                                                    auth_uuid=00000000,
                                                    auth_access_token=00000000,
                                                    user_type='Legacy',
                                                    version_type='Legacy')
        return Launcher.template_script.format(javaw='javaw',
                                               extra=self.extra_argument,
                                               maxmem=maxmem,
                                               native='',
                                               libs=libraries,
                                               main=version.main_class,
                                               mcargs=mcargs)

    @staticmethod
    def _extract_native(jar_path):
        'Extract native files from a jar file'
        with ZipFile(jar_path) as zip:
            pass

if __name__ == '__main__':
    launcher = Launcher(r'C:\Users\Xiaoqin\Documents\Minecraft\.minecraft')
    # print(launcher.version_dict.keys())
    print(launcher.launch('1.11.2'))
