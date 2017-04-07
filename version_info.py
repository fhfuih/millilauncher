import library_info

class VersionInfo(object):
    def __init__(self, d):
        'Initialize a VersionInfo object by a dict parsed from <version>.json'
        self.id = d['id']
        self.minecraft_arguments = d.get('minecraftArguments').replace('$', '')
        self.assets = d.get('assets')
        self.jar = d.get('jar', self.id)
        self.main_class = d.get('mainClass')

        self.libraries = []
        for item in d.get('libraries', []):
            libs = library_info.from_dict(item)
            for lib in libs:
                if lib:
                    self.libraries.append(lib)

        self.inherits_from = d.get('inheritsFrom')

    def inherit(self, parent):
        'check if this version has parent, and inherit its data if so'
        if not parent or not self.inherits_from:
            return False
        if parent.id == self.id:
            raise ValueError
        else:
            self.inherits_from = parent.inherits_from
            if not self.minecraft_arguments:
                self.minecraft_arguments = parent.minecraft_arguments
            if not self.assets:
                self.assets = parent.assets
            if not self.jar:
                self.jar = parent.jar
            if not self.main_class:
                self.main_class = parent.main_class
            self.libraries += parent.libraries
            return True

if __name__ == '__main__':
    import json
    import os
    os.chdir(r'C:\Users\Xiaoqin\Documents\Minecraft\.minecraft\versions')
    path = '1.11.2'
    with open(os.path.join(path, path + '.json'), 'r') as f:
        vi = VersionInfo(json.load(f))
        print(len(vi.libraries))
        for lib in vi.libraries:
            print(lib.name)
