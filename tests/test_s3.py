import json

from s3_tools import upload_json_to_s3


def test_upload_json_to_s3(s3_test_bucket):
    fdata = {"data": "Lorem ipsum", "foo": "bar"}
    object_id = '123456'
    upload_json_to_s3(fdata, object_id)

    expected_object_path = 'path/to/123456.json'
    bucket_object = s3_test_bucket.Object(expected_object_path)
    object_body = bucket_object.get()['Body']
    data = json.loads(object_body.read())
    assert data == {"data": "Lorem ipsum", "foo": "bar"}
