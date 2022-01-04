import requests
import json
import random
import urllib
import string
import base64
import auth
import logging
import spotify
import datetime

# ---functions---


def load_config():
    with open('config.json', 'rb') as f:
        config = json.load(f)

    return config


def set_logger(global_stuff):
    FORMAT = '[%(created)s][%(levelname)s] %(message)s'
    logging.basicConfig(format=FORMAT)
    global_stuff['logger'] = logging.getLogger()
    global_stuff['logger'].setLevel(20)
    return global_stuff


def main():
    global_stuff = load_config()
    global_stuff = set_logger(global_stuff)
    global_stuff['logger'].info('Starting the authentication Process')

    global_stuff = auth.full_auth(global_stuff)
    albums = spotify.get_albums(global_stuff,[])

    yesterday = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(3), '%Y-%m-%d')
    albums = filter(lambda x : x['release_date'] == yesterday, albums)
    tracks = spotify.get_tracks(global_stuff, albums)

    spotify.put_tracks_into_playlist(global_stuff, tracks)


if __name__ == "__main__":
    main()
