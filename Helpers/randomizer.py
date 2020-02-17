import random
import uuid


def rand_track(obj):
    return random.choice(obj.tracks)


def get_list_of_random_tracks_uri(list_of_artists):
    return [rand_track(artist)['uri'] for artist in list_of_artists]


def randomize_name():
    return uuid.uuid4().hex
