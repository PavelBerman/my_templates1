import logging

from sqlalchemy.dialects.mysql import Insert

from db_definitions import MyTable1
from db_handlers import get_db_session

logger = logging.getLogger(__name__)


def write_result_to_db(item_id: int, item_name: str, item_category, properties) -> None:
    with get_db_session() as session, session.begin():
        stmt = Insert(MyTable1).values(item_id=item_id, item_name=item_name, item_category=item_category,
                                       item_properties=properties)
        session.execute(stmt)
        logger.info(f"Inserted item to db: {item_id}, {item_name}, {item_category}, {properties}")
