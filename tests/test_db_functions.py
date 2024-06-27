from unittest import mock

from db_definitions import MyTable1
from db_funcs import write_result_to_db
from db_handlers import get_test_db_session


@mock.patch('db_funcs.get_db_session', side_effect=get_test_db_session)
def test_write_something_to_db(session_mock, test_db_session):
    sample_id = 1
    sample_name = "sample_name"
    sample_category = "my_category"
    calculation_result = {"result": 42}
    write_result_to_db(sample_id, sample_name, sample_category, calculation_result)

    session_mock.assert_called_once()

    with get_test_db_session() as session:
        res = session.query(MyTable1).scalar()
        assert res.item_id == sample_id
        assert res.item_name == sample_name
        assert res.item_category == sample_category
        assert res.item_properties == calculation_result
