from Helpers import reader, randomizer
from Queries import query
from Albums.album import Albums
from Artitsts.artist import Arist



token = ""      # token will expire frequently so it need to be changed
user_id = ""    # insert your spotify username here
names_path = "" # insert pat to file with names of artists here
api_url = 'https://api.spotify.com/v1'
artists_names_list = reader.get_list_from_file(names_path)
random_name = randomizer.randomize_name()
print('Your new playlist is named:', random_name)
artist_list = []
for artist in artists_names_list:
    artist_json = query.get_arist_data(token, api_url, artist)
    albums_json = query.get_album_data(token, api_url, artist_json)
    albums_list = []
    for album in albums_json['items']:
        tracks__json = query.get_albums_tracks(token, api_url, album)
        album_tracks = [{'uri': t['uri'], 'name': t['name']} for t in tracks__json['items']]
        album = Albums(album['name'], album['id'], artist_json['name'], album_tracks)
        albums_list.append(album)
    artist_obj = Arist(artist_json['name'], artist_json['id'],
                       albums_list, [track for alb in albums_list for track in alb.tracks])
    artist_list.append(artist_obj)
list_of_songs = randomizer.get_list_of_random_tracks_uri(artist_list)
playlist_json = query.create_empty_playlist(token, api_url, user_id, random_name)
final_response = query.add_tracks_to_playlist(token, api_url, playlist_json['id'], list_of_songs)
