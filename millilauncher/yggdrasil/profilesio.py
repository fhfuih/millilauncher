import os
import json
import shutil

import yggdrasil.authdata
import dirs


class ProfilesIO:
    def __init__(self):
        with open(dirs.launcherprofiles) as fp:
            self.data = json.load(fp)
            self.authdb = yggdrasil.authdata.AuthenticationDatabase(self.data)

    def save(self):
        if not os.path.exists(dirs.launcherprofiles_backup):
            shutil.copyfile(
                dirs.launcherprofiles, dirs.launcherprofiles_backup)
        self.data['clientToken'] = self.authdb.client_token
        self.data['authenticationDatabase'] = self.authdb.export_database()
        self.data['selectedUser']['account'] = self.authdb.selected_id
        self.data['selectedUser']['profile'] = self.authdb.selected().profile.id
        with open(dirs.launcherprofiles, 'w') as fp:
            json.dump(self.data, fp)


profilesio = ProfilesIO()
