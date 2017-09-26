import json
from . import request

class AuthPartialLaunchArguments(dict):
    pass

class AuthProfileData:
    def __init__(self, name, id, legacy):
        self.id = id
        self.name = name
        self.uuid = '-'.join((id[0:8], id[8:12], id[12:16], id[16:20], id[20:32]))
        self.legacy = legacy
    def export(self):
        if self.legacy:
            return {
                self.id:{
                    'displayName':self.name,
                    'legacy':True
                }
            }
        else:
            return {
                self.id: {
                    'displayName': self.name
                }
            }

class AuthUserProperties(list):
    def __str__(self):
        return json.dumps({x['name']: [x['value']] for x in self})

class AuthUserData:
    # def __init__(self, data, id=None, format=None):
    def __init__(self, data, **kwargs):
        if isinstance(data, request.Response):
            self.access_token = data['accessToken']
            self.username = kwargs.get('username')
            self.properties = AuthUserProperties(data['user']['properties'])
            self.userid = data['user']['id']
            profile = data['selectedProfile']
            self.profile = AuthProfileData(profile['name'], profile['id'], profile.get('legacy', False))
        else: # isinstance(data, authenticationDatabaseObject)
            id, format = kwargs['id'], kwargs['format']
            if format == 20:
                self.access_token = data['accessToken']
                self.username = data['username']
                self.properties = AuthUserProperties(data['properties'])
                self.userid = id
                profile, = data['profiles'].items()
                self.profile = AuthProfileData(profile[1]['displayName'], profile[0], profile[1].get('legacy', False))
            else: # 18 or 17
                self.access_token = data['accessToken']
                self.username = data['username']
                self.properties = AuthUserProperties(data['userProperties'])
                self.userid = data['userid']
                self.profile = AuthProfileData(data['displayName'], id, data.get('legacy', False))
    def generate(self):
        return AuthPartialLaunchArguments({
            'auth_player_name':self.profile.name,
            'auth_uuid':self.profile.uuid,
            'auth_access_token':self.access_token,
            'user_type':'legacy' if self.profile.legacy else 'mojang',
            'user_properties':str(self.properties)
        })

    def export(self):
        return {
            'accessToken': self.access_token,
            'username': self.username,
            'properties': self.properties,
            'profiles': self.profile.export()
        }

class AuthenticationDatabase:
    def __init__(self, data):
        self.client_token = data.get('clientToken')
        self.format = data['launcherVersion']['format']
        if self.format < 20:
            selected_profile = data['selectedUser']
            self.selected_id = data['authenticationDatabase'][selected_profile]['userid']
            self.users = {}
            for x, y in data['authenticationDatabase'].items():
                self.users[y['userid']] = AuthUserData(y, id=x, format=self.format)
        elif self.format == 20:
            self.selected_id = data['selectedUser']['account']
            self.users = {x: AuthUserData(y, id=x, format=self.format) for x, y in data['authenticationDatabase'].items()}
        else:
            raise ValueError('Unsupported launcher_profile format.')


    def append(self, response, username):
        user = AuthUserData(response, username=username)
        userid = user['userid']
        self.users['userid'] = user
        return self.select(userid)

    def update(self, response):
        userid = response['user']['id']
        self.users[userid].access_token = response['accessToken']
        self.users[userid].profile.name = response['selectedProfile']['name']
        self.users[userid].profile.legacy = response['selectedProfile'].get('legacy', False)
        self.users[userid].properties = response['user']['properties']
        if self.client_token is None:
            self.client_token = response['clientToken']
        return self.select(userid)

    def select(self, userid):
        self.selected_id = userid
        return self.selected()

    def selected(self):
        return self.users[self.selected_id]

    def export_database(self):
        return {x: y.export() for x, y in self.users.items()}
