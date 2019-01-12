import logging

from flask import Flask, request

from discogs_py.engine import json_utils
from discogs_py.engine.discogs import Discogs

api = Flask(__name__)
discogs_search_engine = Discogs()


@api.route('/api/discogs/random-song-by-genre', methods=['POST'])
def random_song_by_genre():
    try:
        json_request = request.get_json()
        genre = json_request['genre']
        random_track = discogs_search_engine.get_random_track_by_genre(genre)
        if random_track is None:
            return json_utils.create_json_error_response(-1, 'Track not found', 400)
        else:
            result = {"random_track": random_track}
            return json_utils.create_json_response(result)
    except Exception as e:
        logging.error('Error searching Discogs for track: %s', e.message)
        return json_utils.create_json_error_response(-1, e.message, 400)


@api.route('/api/discogs/random-song-by-artist', methods=['POST'])
def random_song_by_artist():
    try:
        json_request = request.get_json()
        artist_name = json_request['artist']
        random_track = discogs_search_engine.get_random_track_by_artist(artist_name)
        if artist_name is None:
            return json_utils.create_json_error_response(-1, 'Track not found', 400)
        else:
            result = {"random_track": random_track}
            return json_utils.create_json_response(result)
    except Exception as e:
        logging.error('Error searching Discogs for track: %s', e.message)
        return json_utils.create_json_error_response(-1, e.message, 400)
