from sqlalchemy import Column, Integer, String
from db_config import Base  # Import shared Base


def create_dynamic_model(model_class, table_name):
    """ Dynamically assigns a table name to an ORM model """
    class DynamicModel(Base, model_class):  # Base must come first for proper ORM mapping
        __tablename__ = table_name
    return DynamicModel

class CharactersList:
    row = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

class ThreadsList:
    row = Column(Integer, primary_key=True)
    thread = Column(String, nullable=False)

class Characters:
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    race = Column(String, nullable=False)
    age = Column(String, nullable=False)
    role_profession = Column(String, nullable=False)
    social_status = Column(String, nullable=False)
    economic_status = Column(String, nullable=False)

class Threads:
    id = Column(Integer, primary_key=True)
    thread = Column(String, nullable=False)