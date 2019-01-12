import logging

from flask import Flask, request

from youtube_search.engine import json_utils
from youtube_search.engine.youtube import YouTube

api = Flask(__name__)
youtube_search_engine = YouTube()


@api.route('/api/youtube-search-engine', methods=['POST'])
def search_youtube():
    try:
        json_request = request.get_json()
        search_string = json_request['search_string']
        feeling_lucky = json_request['feeling_lucky']
        youtube_video = youtube_search_engine.search_video(search_string, feeling_lucky=feeling_lucky)
        if youtube_video is None:
            return json_utils.create_json_error_response(-1, 'Video not found', 400)
        else:
            result = {"youtube_video": youtube_video}
            return json_utils.create_json_response(result)
    except Exception as e:
        logging.error('Error searching YouTube: %s', e.message)
        return json_utils.create_json_error_response(-1, e.message, 400)
