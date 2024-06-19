import json
import logging

from api_example import call_my_api
from business_logic import calculate_something
from db_funcs import write_result_to_db
from s3_tools import upload_json_to_s3

# Init logger outside of handler to avoid duplicate loggers
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """This is a sample Lambda function. Add and erase relevant parts to apply your desired functionality."""
    logging.info(f"event: {event}")
    logging.info(f"context: {context}")

    sample_id = event.get("body", {}).get("sample_id", -1)
    sample_name = event.get("body", {}).get("sample_name")
    sample_category = event.get("body", {}).get("sample_category")
    data_for_api = event.get("body", {}).get("data", {})
    try:
        response = call_my_api(data_for_api)
        calculation_result = calculate_something(response)
        upload_json_to_s3(calculation_result, sample_id)
        write_result_to_db(sample_id, sample_name, sample_category, calculation_result)
        return {
            "statusCode": 200,
            "body": json.dumps(calculation_result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Something went wrong: {str(e)}")
        }
