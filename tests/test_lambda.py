import json
from unittest import mock

import responses

from api_example import MY_API_URL
from lambda_function import lambda_handler


@responses.activate
@mock.patch('db_funcs.Session')
def test_lambda_handler(db_session_mock, s3_test_bucket):
    responses.post(MY_API_URL, json={
        "body": "Great success!",
        "data": 42
    }, status=200)

    event = {
        "calculate_something": True,
        "body": {
            "sample_id": "1234",
            "sample_name": "test_sample",
            "sample_category": "test_category",
            "data": {
                "x": 5,
                "y": 6
            }
        }
    }

    res = lambda_handler(event=event, context=None)
    assert res['statusCode'] == 200
    body = json.loads(res['body'])
    assert body['data'] == 42
