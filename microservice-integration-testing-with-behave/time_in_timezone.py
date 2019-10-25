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


@app.route('/ping')
def ping():
    """Determine if the service is healthy and serving"""
    requestor = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logger.info(f"Health check requested by ip='{requestor}'")
    return make_response(
        jsonify(status="Serving",
                body="pong"), 200)


@app.route('/help')
def get_help():
    """Return a helpful message"""
    body = 'Accepted args:' \
           '\n\ttimezone: (required)' \
           '\n\tformat: (optional)' \
           '\nExample: {"timezone": "UTC", "format": "MM/dd/yyyy hh:mm tt"}'
    return make_response(
        jsonify(status='OK',
                body=body), 200)


@app.route('/get-time', methods=['POST'])
def post():
    """Get the time at a given timezone"""
    if flask.request.content_type != 'application/json':
        logger.error(f"Request data type is not json (content_type="
                     f"'{flask.request.content_type}')")
        return make_response(
            jsonify(status="Error",
                    errors=['Only JSON data is supported']), 415)

    errors = []
    body = None
    code = 417  # default to bad data status code unless it passes

    req = request.get_json()
    try:
        tz = pytz.timezone(req['timezone'])
        answer = datetime.datetime.now(tz=tz)
        fmt = req.get('format', "yyyy-MM-dd hh:mm:ss tt")
        body = answer.strftime(fmt)

    # If the user passes an unknown timezone, we need to handle it gracefully
    except UnknownTimeZoneError:
        msg = f"Bad timezone received: '{req['timezone']}'"
        errors.append(msg)
        logger.error(msg)

    # We can get a keyerror if 'timezone' is not provided in the request
    except KeyError:
        logger.error(f"Received KeyError: {req}")
        errors.append("'timezone' is a required field")

    if errors:
        return make_response(
            jsonify(status='Error',
                    errors=errors), code)

    # Otherwise everything is good!
    return make_response(
        jsonify(status='OK',
                body=body), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
