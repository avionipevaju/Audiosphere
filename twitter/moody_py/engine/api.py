import logging
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
    logging.info("Received twitter post request with body %s", request.get_json())
    if os.environ['validate_requests'] == 'False':
        logging.warn('Moody isn\'t validating requests!')
        twitter_response = moody.tweet(twitter_request)
        logging.info("Twitter response %s", twitter_response)
        return json_utils.create_json_response(twitter_response, simple=True)
    else:
        if moody.validate_request(twitter_request, request.headers['Authorization']):
            twitter_response = moody.tweet(twitter_request)
            logging.info("Twitter response for post tweet request %s", twitter_response)
            return json_utils.create_json_response(twitter_response, simple=True)
        else:
            logging.info('Bad credentials!')
            return json_utils.create_json_error_response(-1, "Unauthorized!", 401)


@api.route('/moody-py/api/mood', methods=['POST'])
def mood():
    """
    Returns a genre for a given weather condition code.
    :return:Response: Json object with one field genre.
    """
    twitter_request = TwitterRequest(request.get_json())
    logging.info("Received twitter mood request with body %s", request.get_json())
    if os.environ['validate_requests'] == 'False':
        logging.warn('Moody isn\'t validating requests!')
        genre = moody.mood(twitter_request)
        result = {"genre": genre}
        logging.info("Twitter response for mood search %s", result)
        return json_utils.create_json_response(result)
    else:
        if moody.validate_request(twitter_request, request.headers['Authorization']):
            genre = moody.mood(twitter_request)
            result = {"genre": genre}
            return json_utils.create_json_response(result)
        else:
            logging.info('Bad credentials!')
            return json_utils.create_json_error_response(-1, "Unauthorized!", 401)
