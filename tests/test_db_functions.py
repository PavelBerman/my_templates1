from unittest import mock

from db_funcs import write_result_to_db


@mock.patch('db_funcs.Session')
def test_write_something_to_db(session_mock):
    sample_id = 1
    sample_name = "sample_name"
    sample_category = "my_category"
    calculation_result = {"result": 42}
    write_result_to_db(sample_id, sample_name, sample_category, calculation_result)

    session_mock.assert_called_once()
