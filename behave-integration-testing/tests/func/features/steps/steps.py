# -*- coding: utf-8 -*-

from behave import given, when, then
from datetime import timedelta
import requests
import time
import json
import os


class AwaitTimeout(BaseException):
    pass


@given('the flask server is ready')
def wait_for_server(context):
    if hasattr(context, "ready"):
        return

    print("Waiting for the Flask server to start")
    await_sec = int(os.environ['AWAIT_SECONDS'])
    await_timeout = timedelta(milliseconds=await_sec * 1000)
    running_timeout = timedelta(milliseconds=0)
    while True:
        if running_timeout > await_timeout:
            raise AwaitTimeout("Waited too long for server to start")

        # try to ping the healthcheck endpoint
        response = requests.get('http://timezone-app-test:9000/ping')
        if response.status_code == 200:
            break

        running_timeout += timedelta(milliseconds=10)
        time.sleep(0.01)

    print("Server is ready")
    context.ready = True



