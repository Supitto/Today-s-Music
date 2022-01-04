import requests
import urllib
import random
import base64
import string

def full_auth(config):
    url = gen_login_url(config)
    
    print('Please access this URL and paste the results...', url)

    response = input('> ')
    config = process_auth_response_and_get_token(config, response)

    return config


def gen_login_url(config):
    state = ''.join([random.choice(string.ascii_letters) for _ in range(16)])
    scope = 'playlist-modify-private user-read-private playlist-read-private playlist-modify-private playlist-modify-public'
    url = 'https://accounts.spotify.com/authorize?'

    payload = {
        'response_type': 'code',
        'client_id': config['client_id'],
        'scope': scope,
        'redirect_uri': config['redirect_uri'],
        'state': state}

    url += urllib.parse.urlencode(payload, quote_via=urllib.parse.quote_plus)

    return url


def process_auth_response_and_get_token(config, response):
    response_as_dict = {urllib.parse.unquote(k): urllib.parse.unquote(
        v) for [k, v] in [i.split('=') for i in response.split('&')]}

    headers = {
        'Authorization': 'Basic '+base64.b64encode(config['client_id'].encode()+b':'+config['client_secret'].encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': response_as_dict['code'],
        'redirect_uri': config['redirect_uri']
    }

    r = requests.post('https://accounts.spotify.com/api/token',
                      headers=headers, data=data)
    token = r.json()["access_token"]
    refresh_token = r.json()['refresh_token']

    config['token'] = token
    config['refresh_token'] = refresh_token
    config['headers'] = {
        'Authorization': 'Bearer '+token
    }
    return config
