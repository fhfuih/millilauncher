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
import re
from string import Template
from .systeminfo import system, architecture, version

class MCLibrary(object):
    def __init__(self, d):
        self.name = d['name']

        # self.allow
        self.allow = MCLibrary._parse_rule(d)

        if self.allow:
            # self.url, self.path
            native_key = Template(d['natives'][system]).substitute(
                arch=architecture) if 'natives' in d else None
            if 'downloads' in d: # Mojang format
                if native_key:
                    self.url = d['downloads']['classifiers'][native_key]['url']
                    self.path = d['downloads']['classifiers'][native_key]['path']
                    self.sha1 = d['downloads']['classifiers'][native_key]['sha1']
                # make sure non-native is always the fallback option
                else:
                    self.url = d['downloads']['artifact']['url']
                    self.path = d['downloads']['artifact']['path']
                    self.sha1 = d['downloads']['artifact']['sha1']
            else: # Forge format
                url = d.get('url', 'https://libraries.minecraft.net/')
                self.path = MCLibrary._parse_name(self.name, native_key)
                self.url = url + self.path
                self.sha1 = None
                # When (and only when) 'checksum' contains 2 values, neither of them matches its sha1 or md5. Why?

            # self.exclude
            self.exclude = d['extract']['exclude'] if 'extract' in d else []

    @staticmethod
    def _parse_rule(d):
        allow = True
        if 'rules' in d:
            for action_dict in d['rules']: # d['rules'] is a list of dicts
                # if action_dict['action'] == 'allow' and 'os' NOT in: default True, skip.
                if action_dict['action'] == 'allow' and 'os' in action_dict:
                    if system == action_dict['os']['name']:
                        pattern = action_dict['os'].get('version')
                        if pattern:
                            allow = re.match(pattern, version)
                        else:
                            allow = True
                    else:
                        allow = False
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
