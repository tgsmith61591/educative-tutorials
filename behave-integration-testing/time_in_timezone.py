# -*- coding: utf-8 -*-

"""
This service will return the current time in a given timezone
"""

import logging
import datetime
import sys

import flask
from flask import jsonify, make_response, request

import pytz
from pytz.exceptions import UnknownTimeZoneError

app = flask.Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Prints to stdout so we can debug captured logging in behave...
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the service is healthy and serving"""
    requestor = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logger.info(f"Health check requested by ip='{requestor}'")
    content = {'status': 'OK', 'body': 'pong'}
    return flask.Response(content,
                          status=200,
                          mimetype='application/json')


@app.route('/help', methods=['GET'])
def help():
    """Return a helpful message"""
    body = 'Accepted args:' \
           '\n\ttimezone: (required)' \
           '\n\tformat: (optional)' \
           '\nExample: {"timezone": "UTC", "format": "MM/dd/yyyy hh:mm tt"}'
    content = {'status': 'OK', 'body': body}
    return flask.Response(content,
                          status=200,
                          mimetype='application/json')


@app.route('/get-time', methods=['POST'])
def post():
    """Get the time at a given timezone"""
    if flask.request.content_type != 'application/json':
        logger.error(f"Request data type is not json (content_type="
                     f"'{flask.request.content_type}')")
        return make_response(
            jsonify({"status": "Error",
                     "errors": ['Only JSON data is supported']}), 415)

    errors = []
    body = None
    code = 417

    req = request.get_json()
    try:
        tz = pytz.timezone(req['timezone'])
        answer = datetime.datetime.now(tz=tz)
        fmt = req.get('format', "yyyy-MM-dd hh:mm:ss tt")
        body = answer.strftime(fmt)

    except UnknownTimeZoneError:
        msg = f"Bad timezone received: '{req['timezone']}'"
        errors.append(msg)
        logger.error(msg)

    except KeyError:
        logger.error(f"Received KeyError: {req}")
        errors.append("'timezone' is a required field")

    else:
        code = 200

    response = {'status': 'OK' if not errors else 'Error'}
    if errors:
        response['errors'] = errors
    else:
        response['body'] = body
    return make_response(jsonify(response), code)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
