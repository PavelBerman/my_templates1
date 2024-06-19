from sqlalchemy import Column, String, Integer, DateTime, JSON, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class MyTable1(Base):
    __tablename__ = 'my_table_1'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, nullable=False)
    item_name = Column(String(32), nullable=True)
    item_category = Column(String(32), nullable=False)
    item_properties = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"MyTable1(item_id={self.item_id!r}, item_name={self.item_name!r}, " \
               f"item_category={self.item_category!r}, item_properties={self.item_properties!r}, " \
               f"created_at={self.created_at!r}, updated_at={self.updated_at!r})"


index1 = Index("table1_id_category_index", MyTable1.item_category, MyTable1.item_id)
unique1 = Index("table1_id_category_id_unique", MyTable1.item_category, MyTable1.item_id, unique=True)
