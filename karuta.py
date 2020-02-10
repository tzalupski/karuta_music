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
            album_tracks = [(t['uri'], t['name']) for t in tracks_response.json()['items']]
            album = Albums(item['name'], item['id'], get_dict_item(artist_resp,'name'), album_tracks)
            tmp_albums_list.append(album)
        artist_obj =  Arist(get_dict_item(artist_resp,'name'), get_dict_item(artist_resp,'id'), tmp_albums_list, [track for alb in tmp_albums_list for track in alb.tracks])
        artist_list.append(artist_obj)
    return artist_list


def select_songs_at_random(list_of_artists):
    return [random.choice(artist.tracks)[0] for artist in list_of_artists]


def create_empty_playlist(token, user_id, playlist_name):
    query = 'https://api.spotify.com/v1/users/{}/playlists'.format(user_id)
    request_body = json.dumps({
          "name": playlist_name,
          "description": "Karuta_generated_playlist",
          "public": False
        })
    playlist_response = requests.post(url = query, data = request_body,
                                      headers={"Content-Type":"application/json",
                                      "Authorization": "Bearer {}".format(token)}
                                      )
    return  playlist_response.json()


def add_tracks_to_playlist(token, playlist_id, tracks_list):
    query = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
    tracks_query = "?uris={}".format(','.join(tracks_list))
    query = query + tracks_query
    playlist_response = requests.post(url = query,
                                      headers={"Content-Type":"application/json",
                                      "Authorization": "Bearer {}".format(token)}
                                      )
    return playlist_response


#TODO It works!
# token will expire frequently so it need to be changed
token = ""
user_id = "" # TODO insert your spotify username here
random_name = uuid.uuid4().hex
print('Your new playlist is named:', random_name)
artist_list = download_needed_data(token)
list_of_songs = select_songs_at_random(artist_list)
playlist_json = create_empty_playlist(token, user_id,random_name)
final_response = add_tracks_to_playlist(token, playlist_json['id'], list_of_songs)


