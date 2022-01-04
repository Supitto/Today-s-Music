import time
import requests


def get_albums(config, tags):
    albums = []

    response = {'albums': {
        'next': 'https://api.spotify.com/v1/search?type=album&q=tag:new&limit=10'}}
    while 'albums' in response and response['albums']['next'] != None:
        r = requests.get(response['albums']['next'], headers=config['headers'])
        if 'error' in r.json():
            if r.json()['error']['status'] == 404:
                break
            print(r.json(), response['albums']['next'])
            time.sleep(30)
            r = requests.get(response['albums']['next'],
                             headers=config['headers'])
        response = r.json()
        albums += [i for i in response['albums']['items']]

    return albums


def get_tracks(config, albums):
    tracks = []

    for a in albums:
        r1 = requests.get('https://api.spotify.com/v1/albums/' +
                          a['id']+"?limit=50", headers=config['headers'])
        if 'tracks' not in r1.json():
            time.sleep(30)
            r1 = requests.get('https://api.spotify.com/v1/albums/' +
                              a['id']+"?limit=50", headers=config['headers'])
        for t in r1.json()['tracks']['items']:
            r2 = requests.get(t['href'], headers=config['headers'])
            
            if 'error' not in r2.json():
                tracks.append(r2.json()['uri'])
            else:
                print("sleeping")
                time.sleep(30)
                r2 = requests.get(t['href'], headers=config['headers'])
                
                tracks.append(r2.json()['uri'])

    tracks = list(set(tracks))
    return tracks


def put_tracks_into_playlist(config, tracks):
    print(len(tracks))
    for i in range(0, len(tracks), 90):
        data = {
            'uris': tracks[i:i+90],
            'position': 0
        }

        r = requests.post('https://api.spotify.com/v1/playlists/' +
                          config['playlist_id']+'/tracks', json=data, headers=config['headers'])
        print(r, r.text)
