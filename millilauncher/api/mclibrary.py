"""
An object to handle a single library dependency.

Note that since a certain MC version, 'lwjgl-platform' declares both
a 'classifier' key(for native file) and an 'artifact' key(for universal file).
The universal file does exist and is accessible in Mojang's server, but is empty.

There's no such file in official lwjgl binary release either.

So I currently disable the 'both' result in the native-or-not check,
which will be replaced by 'native'.

Further investigation is needed.
"""

from .systeminfo import system, architecture

class MCLibrary(object):
    def __init__(self, d):
        self.name = d['name']

        # self.allow
        self.allow = MCLibrary._parse_rule(d)

        # self.url, self.path, self.url, self.path
        native_key = d['natives'][system].replace('$', '').format(arch=architecture) if 'natives' in d else None
        if 'downloads' in d:
            if native_key:
                self.url = d['downloads']['classifiers'][native_key]['url']
                self.path = d['downloads']['classifiers'][native_key]['path']
            # make sure non-native is always the fallback option
            else: # 'artifact' in d['downloads']
                self.url = d['downloads']['artifact']['url']
                self.path = d['downloads']['artifact']['path']
        else:
            url = d.get('url', 'https://libraries.minecraft.net/')
            self.path = MCLibrary._parse_name(self.name, native_key)
            self.url = url + self.path

        # self.exclude
        self.exclude = d['extract']['exclude'] if 'extract' in d else []

    @staticmethod
    def _parse_rule(d):
        allow = True
        if 'rules' in d:
            for action_dict in d['rules']: # d['rules'] is a list of dicts
                # if action_dict['action'] == 'allow' and 'os' NOT in: default True, skip.
                if action_dict['action'] == 'allow' and 'os' in action_dict:
                    allow = (system == action_dict['os']['name'])
                elif action_dict['action'] == 'disallow':
                    allow = (system != action_dict['os']['name'])
        return allow

    @staticmethod
    def _parse_name(name, native):
        package, name, version = name.split(':')
        if native:
            return '{0}/{1}/{2}/{1}-{2}-{3}.jar'.format(package.replace('.', '/'),
                                                        name,
                                                        version,
                                                        native)
        else:
            return '{0}/{1}/{2}/{1}-{2}.jar'.format(package.replace('.', '/'),
                                                    name,
                                                    version)
