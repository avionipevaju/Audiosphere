import logging

from flask import Flask, request

from yahoo_weather.core import json_utils
from yahoo_weather.core.forecast import Forecast

api = Flask(__name__)


@api.route('/api/yahoo-weather', methods=['POST'])
def get_weather():
    try:
        json_request = request.get_json()
        logging.info("Received yahoo weather request with body %s", json_request)
        location = json_request['location']
        forecast = Forecast(location)
        current_weather = forecast.current_weather()
        logging.info("Yahoo weather response for location %s is %s", location, current_weather)
        return json_utils.create_json_response(forecast.current_weather())
    except Exception as e:
        logging.error('Error while getting the current weather conditions %s', e.message)
        return json_utils.create_json_error_response(-1, e.message, 400)
