import os
import json
import shutil

from . import authdata

FILE_PATH = 'launcher_profiles.json'
BACKUP_PATH = 'launcher_profiles.json.millibackup'

class ProfilesIO:
    def __init__(self):
        with open(FILE_PATH) as fp:
            self.data = json.load(fp)
            self.authdb = authdata.AuthenticationDatabase(self.data)

    def save(self):
        if not os.path.exists(BACKUP_PATH):
            shutil.copyfile(FILE_PATH, BACKUP_PATH)
        self.data['clientToken'] = self.authdb.client_token
        self.data['authenticationDatabase'] = self.authdb.export_database()
        self.data['selectedUser']['account'] = self.selected_id
        self.data['selectedUser']['profile'] = self.selected().profile.id
        with open(FILE_PATH, 'w') as fp:
            json.dump(self.data, fp)
