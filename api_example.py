import requests

MY_API_URL = "https://my-api.com/aa"
MY_API_KEY = "1234567890"


def call_my_api(data):
    res = requests.post(MY_API_URL, data=data, params={'x-api-key': MY_API_KEY})
    res.raise_for_status()
    return res.json()
