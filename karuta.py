import requests
from Reader import reader
import random
import json
import uuid

class Arist:
    def __init__(self, name='', id='', albums=[],tracks=[]):
        self.name = name
        self.id = id
        self.albums = albums
        self.tracks = tracks
class Albums:
    def __init__(self, name='', id='', artist='',tracks=[]):
        self.name = name
        self.id = id
        self.artist = artist
        self.tracks = tracks

def get_dict_item(dict, key):
    return dict.setdefault(key, {})

#TODO Work in progress
# token will expire frequently so it need to be changed
token = 'BQBHzEvyZC_Cuc72evy8hRYk-dikH9JnFqybR1KVCozpWwUUxmQW8ZnIOiqTTw44Vaq9LhJis-s1jjg3s3W0v53FM4ZV4UfwfkdSM9ionDEIuKnEzKEOc1D577kp6ldXIZbqvxN9mLUQexuTiBpdD26um7MMMxKBol66AOg'

def download_needed_data(token):
    search_url = 'https://api.spotify.com/v1/search'
    artists_names_list = reader.get_list_from_file('tmp_data/artists.txt')
    artist_list = []
    for artist in artists_names_list:
        artist_name = artist.replace(' ','%20')
        artist_query = '{}?q={}&type=artist&limit=1'.format(search_url,artist_name)
        response = requests.get(artist_query, headers={"Content-Type":"application/json",
                               "Authorization": "Bearer {}".format(token)})
        artist_resp  = get_dict_item(get_dict_item(response.json(),'artists'),'items')[0]
        albums_query = 'https://api.spotify.com/v1/artists/{}/albums?include_groups=album,single,compilation'.format(get_dict_item(artist_resp,'id'))
        albums_response = requests.get(albums_query, headers={"Authorization": "Bearer {}".format(token)})
        tmp_albums_list = []
        for item in get_dict_item(albums_response.json(),'items'):
            tracks_query = 'https://api.spotify.com/v1/albums/{}/tracks?limit=50'.format(item['id'])
            tracks_response = requests.get(tracks_query, headers={"Authorization": "Bearer {}".format(token)})
            album_tracks = [{t['name']: t['id']} for t in tracks_response.json()['items']]
            album = Albums(item['name'], item['id'], get_dict_item(artist_resp,'name'), album_tracks)
            tmp_albums_list.append(album)
        artist_obj =  Arist(get_dict_item(artist_resp,'name'), get_dict_item(artist_resp,'id'), tmp_albums_list, [track for alb in tmp_albums_list for track in alb.tracks])
        artist_list.append(artist_obj)

def select_songs_at_random(list_of_artists):
    return [random.choice(artist.tracks)['id'] for artist in list_of_artists]

def create_empty_playlist(token, user_id, playlist_name):
    random_name = uuid.uuid4()
    query = 'https://api.spotify.com/v1/users/{}/playlists'.format(user_id)
    request_body = json.dumps({
          "name": random_name,
          "description": "Karuta_generated_playlist",
          "public": False
        })
    requests.post(url = query, data = request_body, headers={"Content-Type":"application/json",
                               "Authorization": "Bearer {}".format(token)})
