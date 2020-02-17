import json
import requests


def get_arist_data(token, api_url, artist_name):
    artist_name = artist_name.replace(' ', '%20')
    query = '{}/search/?q={}&type=artist&limit=1'.format(api_url, artist_name)
    response = requests.get(query, headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer {}".format(token)})
    artist_json = response.json()['artists']['items'][0]
    return artist_json


def get_album_data(token, api_url, artist_json):
    albums_query = '{}/artists/{}/albums?include_groups=album,single,compilation'\
        .format(api_url, artist_json['id'])
    albums_response = requests.get(albums_query, headers={"Authorization": "Bearer {}".format(token)})
    return albums_response.json()


def get_albums_tracks(token, api_url, album_json):
    tracks_query = '{}/albums/{}/tracks?limit=50'.format(api_url, album_json['id'])
    tracks_response = requests.get(tracks_query, headers={"Authorization": "Bearer {}".format(token)})
    return tracks_response.json()


def create_empty_playlist(token, api_url, user_id, playlist_name):
    query = '{}/users/{}/playlists'.format(api_url, user_id)
    request_body = json.dumps({
          "name": playlist_name,
          "description": "Karuta_generated_playlist",
          "public": False
        })
    playlist_response = requests.post(url=query, data=request_body,
                                      headers={"Content-Type": "application/json",
                                               "Authorization": "Bearer {}".format(token)}
                                      )
    return playlist_response.json()


def add_tracks_to_playlist(token, api_url, playlist_id, tracks_list):
    query = '{}/playlists/{}/tracks'.format(api_url, playlist_id)
    tracks_query = "?uris={}".format(','.join(tracks_list))
    query = query + tracks_query
    playlist_response = requests.post(url=query,
                                      headers={"Content-Type": "application/json",
                                               "Authorization": "Bearer {}".format(token)}
                                      )
    return playlist_response