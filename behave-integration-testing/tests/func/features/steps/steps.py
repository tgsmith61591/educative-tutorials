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


@when('the "{payload}" is posted')
def post_payload(context, payload):
    payload = json.loads(payload)
    response = requests.post('http://timezone-app-test:9000/get-time',
                             data=json.dumps(payload),
                             headers={'Content-type': 'application/json'})
    context.response = response


@then('the status is "{status}"')
def assert_status(context, status):
    response = context.response.json()
    assert response['status'] == status, \
        f"\nExpected: '{status}'" \
        f"\nGot: '{response}'"


@then('the return code is "{return_code}"')
def assert_return_code(context, return_code):
    assert context.response.status_code == int(return_code), \
        f"\nExpected: '{return_code}'" \
        f"\nGot: '{context.status_code}'"


@then('the response contains "{field}"')
def assert_contains_field(context, field):
    response = context.response.json()
    assert field in response, \
        f"\nExpected: '{field}' present" \
        f"\nGot: '{response}'"
