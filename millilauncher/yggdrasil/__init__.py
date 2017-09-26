from . import (request, authdata)

from .profilesio import ProfilesIO

def init():
    profilesio = ProfilesIO()

def login(username, passowrd):
    r = request.login(username, passowrd, profilesio.authdb.client_token)
    print(r)
    payload = profilesio.authdb.append(r, username).generate()
    profilesio.save()
    return payload

def resume():
    data = profilesio.authdb.selected()
    status_ok = request.check(data.access_token, profilesio.authdb.client_token)
    if not status_ok:
        r = request.refresh(data.access_token, profilesio.authdb.client_token)
        print(r)
        payload = profilesio.authdb.update(r).generate()
        profilesio.save()
        return payload
    else:
        return profilesio.authdb.selected().generate()

def offline(playername=None):
    playername = playername or profilesio.authdb.selected().profile.name
    return authdata.AuthPartialLaunchArguments({
        'auth_player_name':playername,
        'auth_uuid':'0',
        'auth_access_token':'0',
        'user_type':'legacy',
        'user_properties':{}
    })
