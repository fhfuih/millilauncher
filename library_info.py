from system_info import system
from copy import deepcopy

class LibraryInfo(object):
    def __init__(self, d):
        self.__dict__.update(dict.fromkeys(['name',
                                            'allow',
                                            'url',
                                            'path',
                                            'native_url',
                                            'native_path',
                                            'exclude']))
        self.name = d['name']

        # self.allow
        self.allow = LibraryInfo._parse_rule(d)

        # self.url, self.path, self.native_url, self.native_path
        native_key = d['natives'][system] if 'natives' in d else None
        if 'downloads' in d:
            if 'artifact' in d['downloads']:
                self.url = d['downloads']['artifact']['url']
                self.path = d['downloads']['artifact']['path']
            if native_key:
                self.native_url = d['downloads']['classifiers'][native_key]['url']
                self.native_path = d['downloads']['classifiers'][native_key]['path']
        else:
            url = d.get('url', 'https://libraries.minecraft.net/')
            if native_key:
                self.native_path = LibraryInfo._parse_name(self.name, native_key)
                self.native_url = url + self.native_path
            else:
                self.path = LibraryInfo._parse_name(self.name)
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
    def _parse_name(name, native=''):
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

def from_dict(d):
    '''returns a tuple of two library object, representing unified and native version.
    return None if doesn\'t exist. '''
    lib1 = LibraryInfo(d)
    if not lib1.allow:
        return None, None
    else:
        lib2 = deepcopy(lib1)
        lib2.path = lib2.native_path
        lib2.url = lib2.native_url
        # print(lib1.path, lib2.path)
        if not lib1.path:
            lib1 = None
        if not lib2.path:
            lib2 = None
        # print(lib1 == None, lib2 == None)
        return lib1, lib2

if __name__ == '__main__':
    vanilla_osx = r'''{
            "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.2-nightly-20140822",
            "rules": [
                {
                    "action": "allow",
                    "os": {
                        "name": "osx"
                    }
                }
            ],
            "downloads": {
                "artifact": {
                    "size": 173887,
                    "sha1": "f0e612c840a7639c1f77f68d72a28dae2f0c8490",
                    "path": "org/lwjgl/lwjgl/lwjgl_util/2.9.2-nightly-20140822/lwjgl_util-2.9.2-nightly-20140822.jar",
                    "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl_util/2.9.2-nightly-20140822/lwjgl_util-2.9.2-nightly-20140822.jar"
                }
            }
        }'''
    vanilla_native = r'''{
            "extract": {
                "exclude": [
                    "META-INF/"
                ]
            },
            "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.2-nightly-20140822",
            "natives": {
                "linux": "natives-linux",
                "osx": "natives-osx",
                "windows": "natives-windows"
            },
            "rules": [
                {
                    "action": "allow",
                    "os": {
                        "name": "osx"
                    }
                }
            ],
            "downloads": {
                "classifiers": {
                    "natives-linux": {
                        "size": 578539,
                        "sha1": "d898a33b5d0a6ef3fed3a4ead506566dce6720a5",
                        "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-linux.jar",
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-linux.jar"
                    },
                    "natives-osx": {
                        "size": 468116,
                        "sha1": "79f5ce2fea02e77fe47a3c745219167a542121d7",
                        "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-osx.jar",
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-osx.jar"
                    },
                    "natives-windows": {
                        "size": 613680,
                        "sha1": "78b2a55ce4dc29c6b3ec4df8ca165eba05f9b341",
                        "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-windows.jar",
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-windows.jar"
                    }
                }
            }
        }'''
    vanilla_both = r'''{
            "extract": {
                "exclude": [
                    "META-INF/"
                ]
            },
            "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.4-nightly-20150209",
            "natives": {
                "linux": "natives-linux",
                "osx": "natives-osx",
                "windows": "natives-windows"
            },
            "rules": [
                {
                    "action": "allow"
                },
                {
                    "action": "disallow",
                    "os": {
                        "name": "osx"
                    }
                }
            ],
            "downloads": {
                "classifiers": {
                    "natives-linux": {
                        "size": 578680,
                        "sha1": "931074f46c795d2f7b30ed6395df5715cfd7675b",
                        "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar"
                    },
                    "natives-osx": {
                        "size": 426822,
                        "sha1": "bcab850f8f487c3f4c4dbabde778bb82bd1a40ed",
                        "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar"
                    },
                    "natives-windows": {
                        "size": 613748,
                        "sha1": "b84d5102b9dbfabfeb5e43c7e2828d98a7fc80e0",
                        "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-windows.jar",
                        "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-windows.jar"
                    }
                },
                "artifact": {
                    "size": 22,
                    "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                    "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                    "url": "https://libraries.minecraft.net/org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar"
                }
            }
        }'''
    legacy = r'''{
      "name": "org.lwjgl.lwjgl:lwjgl_util:2.9.1"
    }'''
    legacy_native = r'''{
      "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.1",
      "natives": {
        "linux": "natives-linux",
        "windows": "natives-windows",
        "osx": "natives-osx"
      },
      "extract": {
        "exclude": [
          "META-INF/"
        ]
      }
    }'''
    mod = r'''{
      "name": "com.typesafe.akka:akka-actor_2.11:2.3.3",
      "url": "http://files.minecraftforge.net/maven/",
      "checksums": [
        "ed62e9fc709ca0f2ff1a3220daa8b70a2870078e",
        "25a86ccfdb6f6dfe08971f4825d0a01be83a6f2e"
      ],
      "serverreq": true,
      "clientreq": true
    }'''
    vanilla_common = r'''        {
            "name": "com.paulscode:codecwav:20101023",
            "downloads": {
                "artifact": {
                    "size": 5618,
                    "sha1": "12f031cfe88fef5c1dd36c563c0a3a69bd7261da",
                    "path": "com/paulscode/codecwav/20101023/codecwav-20101023.jar",
                    "url": "https://libraries.minecraft.net/com/paulscode/codecwav/20101023/codecwav-20101023.jar"
                }
            }
        }
    '''
    import json
    # cm = LibraryInfo(json.loads(vanilla_common))
    # print(cm.path)
    cm = from_dict(json.loads(vanilla_common))[0]
    print(cm.path)
    # lst = [vanilla_both, vanilla_native, vanilla_osx, legacy, legacy_native, mod]
    # for obj in lst:
    #     lb = from_dict(json.loads(obj))
    #     print('=====')
    #     print(lb.name)
    #     print(lb.allow)
    #     print(lb.url)
    #     print(lb.path)
    #     print(lb.native_path)
    #     print(lb.native_url)