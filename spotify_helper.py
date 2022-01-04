import requests
import auth


baseurl = 'ttps://api.spotify.com/v1/'

#This functions believes that you will send http safe characters
#It believes in you
#Don't let her down

def get(config, path, query={}):
    q = '&'.join([f"{k}={v}" for k,v in query.items()])
    r = requests.get(f"{baseurl}{path}?{q}", headers=config['headers'])
    return r.json()

