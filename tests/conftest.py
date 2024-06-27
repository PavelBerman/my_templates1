import os
from pathlib import Path

import boto3
import dotenv
import pytest
from moto import mock_aws

from db_definitions import Base
from db_handlers import test_engine, test_session

local_env_file = Path(__file__) / os.pardir / os.pardir / '.env'
dotenv.load_dotenv(local_env_file, verbose=True)


@pytest.fixture(scope='session')
def s3_test_bucket():
    with mock_aws():
        conn = boto3.resource("s3", region_name=os.getenv('AWS_REGION'))
        bucket = conn.create_bucket(Bucket=os.getenv('S3_BUCKET'))
        yield bucket


@pytest.fixture(scope='function')
def test_db_session():
    os.makedirs(os.path.dirname(test_engine.url.database), exist_ok=True)
    Base.metadata.drop_all(test_engine)  # clean test db before starting

    # Create tables
    Base.metadata.create_all(test_engine)
    yield test_session
