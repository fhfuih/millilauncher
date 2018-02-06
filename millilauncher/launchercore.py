"""
Core Minecraft luancher object.
"""
import logging
import os
import subprocess
from string import Template
from zipfile import ZipFile

import dirs
import yggdrasil
import clientcore.mcversionslist
import download

_template_script = Template('${javaw} ${extra} -Xmx${maxmem}M -Djava.library.path=${natives} -cp ${libs} ${main} ${mcargs}')


class LauncherCore(object):
    """
    Core Minecraft luancher object.
    """
    def __init__(self, mc_dir=dirs.minecraft_dir, java_dir=dirs.java_dir):
        self.minecraft_directory = mc_dir
        self.java_directory = java_dir
        if not mc_dir or not os.path.exists(mc_dir):
            logging.critical('Invalid /.minecraft/ directory.')
            raise FileNotFoundError('Invalid /.minecraft/ directory {0}'.format(mc_dir))
        if not java_dir or not os.path.exists(java_dir):
            logging.critical('Invalid javaw.exe directory.')
            raise FileNotFoundError('Invalid javaw.exe directory {0}'.format(java_dir))
        self.libraries_directory = os.path.join(self.minecraft_directory, 'libraries')
        self.assets_directory = os.path.join(self.minecraft_directory, 'assets')
        self.version_directory = None
        self.natives_directory = None
        self.libraries = None
        os.chdir(self.minecraft_directory)
        self.versions = clientcore.mcversionslist.MCVersionsList(mc_dir)

    def launch(self, version_id, auth_tuple=('Steve', None), maxmem=1024):
        """
        Launch Minecraft
        """
        # subprocess.run(self.launch_raw(version_id, username, maxmem))
        if dirs.system == 'windows':
            p = subprocess.Popen(
                self.launch_raw(version_id, auth_tuple, maxmem),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            from shlex import split
            p = subprocess.Popen(
                split(self.launch_raw(version_id, auth_tuple, maxmem)),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # goal: launch(self, version_id, auth[tuple], maxmem, windows_ize[tuple])
    def launch_raw(self, version_id, auth_tuple, maxmem):
        """
        Returns a command script to launch Minecraft
        """
        logging.info('Attemting to launch Minecraft %s', version_id)
        version = self.versions.get(version_id)  # Success indicates existance of <v>.json and <parent>.json
        self._update_directories(version_id)
        self._update_libraries(version)
        self._extract_natives(version)

        jar = os.path.join(self.minecraft_directory, 'versions', version.jar, version.jar + '.jar')
        libraries = (';' if dirs.system == 'windows' else ':').join(self.libraries) + ';' + jar
        extra_argument = '-Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true' if version.is_forge else None

        mcargs_substitute = dict(
            version_name=version_id,
            game_directory=self.minecraft_directory,
            assets_root=self.assets_directory,
            assets_index_name=version.assets,
            version_type=version.type
        )
        mcargs_substitute.update(self._authorize(auth_tuple))
        mcargs = version.minecraft_arguments.substitute(mcargs_substitute)

        script = _template_script.substitute(
            javaw=self.java_directory, extra=extra_argument, maxmem=maxmem,
            natives=self.natives_directory, libs=libraries, main=version.main_class, mcargs=mcargs)
        logging.info('Successfully generated launching script.')
        return script

    def _update_directories(self, version_id):
        self.version_directory = os.path.join(self.minecraft_directory, 'versions', version_id)
        self.natives_directory = os.path.join(self.version_directory, version_id + '-natives')

    def _extract_natives(self, version):
        os.chdir(self.libraries_directory)
        for library in version.extract:
            with ZipFile(library.path) as libzip:
                namelist = libzip.namelist()
                for excl_name in library.exclude:
                    namelist = [x for x in namelist if not x.startswith(excl_name)]
                libzip.extractall(self.natives_directory, namelist)
                logging.debug('Extracted %d files from library %s', len(namelist), library.name)
        os.chdir(self.minecraft_directory)

    def _update_libraries(self, version):
        self.libraries = []
        for lib in version.libraries:
            full_path = os.path.join(self.libraries_directory, lib.path)
            if not os.path.exists(full_path):
                download.download(lib.url, lib.name, full_path)
            self.libraries.append(full_path)
            logging.debug('Loaded library {0}, path {1}, url {2}'.format(lib.name,full_path, lib.url))
        logging.info('Loaded all libraries. %d in total', len(self.libraries))

    @staticmethod
    def _authorize(auth_tuple):
        if auth_tuple[1] is None:
            return yggdrasil.offline(auth_tuple[0])
        else:
            return yggdrasil.login(*auth_tuple)
