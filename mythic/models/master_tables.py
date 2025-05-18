from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from db_config import Base  # Import shared Base


def create_dynamic_model(model_class, table_name):
    """ Dynamically assigns a table name to an ORM model """
    class DynamicModel(Base, model_class):  # Base must come first for proper ORM mapping
        __tablename__ = table_name
    return DynamicModel

class StoriesIndex:
    index = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))
    modified_date = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
