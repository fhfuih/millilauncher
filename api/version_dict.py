from version_info import VersionInfo
import os
import json

class VersionsDict(dict):
    def __init__(self, path_to_versions_folder='versions'):
        '''Initialize a dict of VersionInfo objects in the given \'versions\' folder
        either set the correct working directory or pass the path to \'versions\''''
        os.chdir(path_to_versions_folder)
        for version in os.listdir():
            if os.path.isdir(version):
                json_file = os.path.join(version, version + '.json')
                if os.path.exists(json_file):
                    with open(json_file) as fp:
                        self[version] = VersionInfo(json.load(fp))
        os.chdir('..')

    def __getitem__(self, key):
        this = dict.__getitem__(self, key)
        parent_key = this.inherits_from
        if not parent_key:
            return this
        parent = self[parent_key] # recursively do parent's inheritance first
        this.inherit(parent)
        return this

if __name__ == '__main__':
    import time
    start = time.time()
    vd = VersionsDict(r'C:\Users\Xiaoqin\Documents\Minecraft\.minecraft\versions')
    print(vd.keys())
    for id in ['1.11.2-LiteLoader1.11.2-1.11.2-forge1.11.2-13.20.0.2228',
               '1.11.2-forge1.11.2-13.20.0.2228',
               '1.11.2']:
        ver = vd[id]
        print('=====')
        print(len(ver.libraries))
    end = time.time()
    print('time', end - start)