from sqlalchemy import Column, Integer, String
from .db_config import Base  # Import shared Base


def create_dynamic_model(model_class, table_name):
    """ Dynamically assigns a table name to an ORM model """
    class DynamicModel(Base, model_class):  # Base must come first for proper ORM mapping
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
    return DynamicModel

class CharactersList:
    row = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    master_id = Column(Integer, nullable=True)

class ThreadsList:
    row = Column(Integer, primary_key=True)
    thread = Column(String, nullable=True)
    master_id = Column(Integer, nullable=True)