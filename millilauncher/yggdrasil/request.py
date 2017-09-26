import json
import requests

LOGIN_URL = 'https://authserver.mojang.com/authenticate'
REFRESH_URL = 'https://authserver.mojang.com/refresh'
CHECK_URL = 'https://authserver.mojang.com/validate'
LOGOUT_URL = 'https://authserver.mojang.com/invalidate'

HEADERS = {
    'content-type': 'application/json'
}

class Response(dict):
    pass

def login(username, password, client_token=None):
    payload = {
        "agent": {
            "name": "Minecraft",
            "version": 1
        },
        "username": username,
        "password": password,
        "requestUser": True # optimize this entry later, maybe?
    }
    if client_token is not None:
        payload.update(clientToken=client_token)
    r = requests.post(LOGIN_URL, json=payload, headers=HEADERS)
    obj = r.json()
    _check_status(r.status_code, obj)
    return Response(obj)

def refresh(access_token, client_token):
    payload = dict(accessToken=access_token, clientToken=client_token)
    r = requests.post(REFRESH_URL, json=payload, headers=HEADERS)
    obj = r.json()
    _check_status(r.status_code, obj)
    return Response(obj)

def check(access_token, client_token):
    payload = dict(accessToken=access_token, clientToken=client_token, requestUser=True)
    r = requests.post(CHECK_URL, json=payload, headers=HEADERS)
    return bool(r)

def logout(access_token, client_token):
    payload = dict(accessToken=access_token, clientToken=client_token)
    r = requests.post(LOGOUT_URL, json=payload, headers=HEADERS)
    obj = r.json()
    _check_status(r.status_code, obj)
    return Response(obj)

def _check_status(code, obj):
    if code != requests.codes.ok:
        obj.setdefault('cause', '')
        msg = '{error}: {errorMessage}. {cause}'.format(**obj)
        raise RuntimeError(msg)
