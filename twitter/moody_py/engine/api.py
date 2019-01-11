import os

from flask import Flask, request

from moody_py.engine import json_utils
from moody_py.engine.model import TwitterRequest
from moody_py.engine.moody import Moody

api = Flask(__name__)
moody = Moody()
moody.verify_credentials()


@api.route('/moody-py/api/post', methods=['POST'])
def post():
    """
    Rest endpoint for posting to Twitter.
    :return: Response: Json represented TwitterResponse object
    """
    twitter_request = TwitterRequest(request.get_json())
    if os.environ['validate_requests'] == 'False':
        twitter_response = moody.tweet(twitter_request)
        return json_utils.create_json_response(twitter_response)
    else:
        if moody.validate_request(twitter_request, request.headers['Authorization']):
            twitter_response = moody.tweet(twitter_request)
            return json_utils.create_json_response(twitter_response)
        else:
            return json_utils.create_json_error_response(-1, "Unauthorized!", 401)


@api.route('/moody-py/api/mood', methods=['POST'])
def mood():
    """
    :return:
    """
    twitter_request = TwitterRequest(request.get_json())
    if os.environ['validate_requests'] == 'False':
        genre = moody.mood(twitter_request)
        result = {"genre": genre}
        return json_utils.create_json_response(result)
    else:
        if moody.validate_request(twitter_request, request.headers['Authorization']):
            genre = moody.mood(twitter_request)
            result = {"genre": genre}
            return json_utils.create_json_response(result)
        else:
            return json_utils.create_json_error_response(-1, "Unauthorized!", 401)
