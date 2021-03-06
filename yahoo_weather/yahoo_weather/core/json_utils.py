import logging

from flask import Response, json, jsonify


def create_json_response(source):
    """
    Creates a response represented in json from a given source
    :param source: Object to represent as json
    :return: Response: Flask Response object
    """
    try:
        if source is None:
            return create_json_error_response(-2, "Response is empty!", 400)
        else:
            return Response(json.dumps(source.__dict__, indent=4, sort_keys=True, default=str), status=200,
                            mimetype='application/json')
    except Exception as e:
        logging.error('Error creating json response from %s', e.message)


def create_json_error_response(code, description, http_status):
    """
    Creates an error response represented in json
    :param code: Error code
    :param description: Error description
    :param http_status: Http status of the response
    :return:
    """
    try:
        response = jsonify(status=code, description=description)
        response.status_code = http_status
        return response
    except Exception as e:
        logging.error('Error creating json error response from %s,', e.message)
