from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from zoneinfo import ZoneInfo
from .db_config import Base  # Import shared Base


IST = ZoneInfo("Asia/Kolkata")  # Define IST timezone

class StoriesIndex(Base):
    __tablename__ = "stories_index"

    index = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    race = Column(String, nullable=True)
    age = Column(String, nullable=True)
    role_profession = Column(String, nullable=True)
    social_status = Column(String, nullable=True)
    economic_status = Column(String, nullable=True)
    story_index = Column(Integer, nullable=True)
    acive = Column(Boolean, default=True)
    image_path = Column(String, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Places(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    weather = Column(String, nullable=True)
    smell = Column(String, nullable=True)
    story_index = Column(Integer, nullable=True)
    acive = Column(Boolean, default=True)    
    image_path = Column(String, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    material = Column(String, nullable=True)
    rarity = Column(String, nullable=True)
    story_index = Column(Integer, nullable=True)
    acive = Column(Boolean, default=True)    
    image_path = Column(String, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Threads(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    thread = Column(String, nullable=True)   
    story_index = Column(Integer, nullable=True)
    acive = Column(Boolean, default=True)    
    image_path = Column(String, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))