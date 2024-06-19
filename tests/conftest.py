import os
from pathlib import Path

import boto3
import dotenv
import pytest
from moto import mock_aws

local_env_file = Path(__file__) / os.pardir / os.pardir / '.env'
dotenv.load_dotenv(local_env_file, verbose=True)


@pytest.fixture(scope='session')
def s3_test_bucket():
    with mock_aws():
        conn = boto3.resource("s3", region_name=os.getenv('AWS_REGION'))
        bucket = conn.create_bucket(Bucket=os.getenv('S3_BUCKET'))
        yield bucket
