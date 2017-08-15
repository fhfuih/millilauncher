import json

class AuthProfileData:
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.uuid = '-'.join((id[0:8], id[8:12], id[12:16], id[16:20], id[20:32]))

class AuthUserProperties(list):
    def __str__(self):
        return json.dumps({x['name']: [x['value']] for x in self})

class AuthUserData:
    def __init__(self, data, id, format):
        if format == 20:
            self.access_token = data['accessToken']
            self.username = data['username']
            self.properties = AuthUserProperties(data['properties'])
            self.userid = id
            (player_id, player_name), = data['profiles'].items()
            self.profile = AuthProfileData(player_name, player_id)
            self.legacy = data.get('legacy', False)
        else: # 18 or 17
            self.access_token = data['accessToken']
            self.username = data['username']
            self.properties = data['userProperties']
            self.userid = data['userid']
            self.profile = AuthProfileData(data['displayName'], id)
            self.legacy = data.get('legacy', False)
    
    def generate(self):
        return {
            'auth_player_name':self.profile.name,
            'auth_uuid':self.profile.uuid,
            'auth_access_token':self.access_token,
            'user_type':'legacy' if self.legacy else 'mojang',
            'user_properties':str(self.properties)
        }

    @staticmethod
    def parse_response(response):
        pass

class AuthenticationDatabase:
    def __init__(self, data):
        if format not in (17, 18, 20):
            raise ValueError('Unsupported launcher_profile format.')
        self.format = data['launcherVersion']['format']
        if format < 20:
            selected_profile = data['selectedUser']
            self.select_id = data['authenticationDatabase'][selected_profile]['userid']

            
            self.data = {}
            for i in data['authenticationDatabase']:
                self.data[i['userid']] = AuthUserData(i)
        else:
            self.select_id = data['selectedUser']['account']


            self.data = {x: AuthUserData(y) for x, y in data['authenticationDatabase']}


    def append(self, response, username):
        user_id = response['user']['id']
        profile = response['selectedProfile']
        if self.format == 20:
            self.data[user_id] = {
                'accessToken':response['accessToken'],
                'username':username,
                'properties':response['user']['properties'],
                'profiles':{
                    profile['id']:{
                        'displayName':profile['name']
                    }
                }
            }
            if profile.get('legacy', False):
                self.data[user_id]['profiles'][profile['id']]['legacy'] = True
        else: # 18 or 17
            uuid = profile['id']
            self.data[uuid] = {
                'accessToken':response['accessToken'],
                'displayName':profile['name'],
                'uuid':'-'.join((uuid[0:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:32])),
                'userProperties':response['user']['properties'],
                'userid':user_id,
                'username':username
            }

    def update(self, response):
        user_id = response['user']['id']
        profile = response['selectedProfile']
        if self.format == 20:
            selected = self.data[user_id]
            selected['accessToken'] = response['accessToken']
            selected['profiles'][profile['id']] = profile['name']
            selected['properties'] = response['user']['properties']
        else: # 18 or 17
            uuid = profile['id']
            selected = self.data[uuid]
            selected['accessToken'] = response['accessToken']
            selected['displayName'] = profile['name']
            selected['userProperties'] = response['user']['properties']

    def select_id(self, profile_id, user_id=None):
        if self.format == 20:
            if user_id is None:
                raise TypeError('User-id not specified.')
            raw_user = self.data.get(user_id)
            if raw_user is None:
                raise ValueError("User of this id hadn't logged in before.")
            raw_profile = raw_user['profiles'].get(profile_id)
            if raw_profile is None:
                raise ValueError("User of this id hadn't logged in before.")
            return {
                'auth_player_name':raw_profile['displayName'],
                'auth_uuid':profile_id,
                'auth_access_token':raw_user['accessToken'],
                'user_type':'legacy' if raw_profile.get('legacy', False) else 'mojang',
                'user_properties':json.dumps(
                    {x['name']: [x['value']] for x in raw_user.get('properties', [])})
            }
        else: # 18 or 17
            raw_user = self.data.get(profile_id)
            if raw_user is None:
                raise ValueError("User of this id hadn't logged in before.")
            return {
                'auth_player_name':raw_user['displayName'],
                'auth_uuid':profile_id,
                'auth_access_token':raw_user['accessToken'],
                'user_type':'legacy' if raw_user.get('legacy', False) else 'mojang',
                'user_properties':json.dumps(
                    {x['name']: [x['value']] for x in raw_user.get('userProperties', [])})
            }
