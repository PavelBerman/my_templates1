import pytest
import responses

from api_example import MY_API_URL, call_my_api


@responses.activate
def test_call_my_api_successful():
    responses.post(MY_API_URL, json={
        "body": "Great success!",
        "data": 42
    }, status=200)

    res = call_my_api({"foo": "bar"})
    assert res["data"] == 42


@responses.activate
def test_call_my_api_failed():
    responses.post(MY_API_URL, json={
        "body": "Not this time my friend",
        "data": -1
    }, status=503)

    with pytest.raises(Exception):
        call_my_api({"foo": "bar"})
