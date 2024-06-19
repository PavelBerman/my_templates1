import json
import os

import boto3

bucket = os.getenv('S3_BUCKET')


def upload_json_to_s3(json_data, fname):
    s3 = boto3.resource('s3')
    bucket_path = f'path/to/{fname}.json'
    s3.Bucket(bucket).put_object(Key=bucket_path, Body=json.dumps(json_data))
