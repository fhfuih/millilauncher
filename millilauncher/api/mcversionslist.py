from mcversion import MCVersion
import os
import json

class MCVersionsList(object):
    def __init__(self, path_to_versions_folder='versions'):
        '''Initialize a dict of MCVersion objects in the given \'versions\' folder
        either set the correct working directory or pass the path to \'versions\''''
        self._dict = {}
        os.chdir(path_to_versions_folder)
        for version in os.listdir():
            if os.path.isdir(version):
                json_file = os.path.join(version, version + '.json')
                if os.path.exists(json_file):
                    with open(json_file) as fp:
                        self._dict[version] = MCVersion(json.load(fp))
        os.chdir('..')

    def get(self, version_id):
        '''Attempt to get a MCVersion object according to its id.
        Returns None if not in the list.'''
        this = self._dict.get(version_id)
        if not this:
            return None
        parent_id = this.inherits_from
        if parent_id:
            parent = self.get(parent_id) # recursively do parent's inheritance first
            this.inherit(parent)
        return this

if __name__ == '__main__':
    vl = MCVersionsList(r'C:\Users\Xiaoqin\Documents\Minecraft\.minecraft\versions')
    print(vl._dict.keys())
    for version in ['1.11.2-LiteLoader1.11.2-1.11.2-forge1.11.2-13.20.0.2228',
                    '1.11.2-forge1.11.2-13.20.0.2228',
                    '1.11.2']:
        ver = vl.get(version)
        print('=====')
        print(len(ver.libraries))