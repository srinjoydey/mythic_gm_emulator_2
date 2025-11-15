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
    chaos_factor = Column(Integer, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    descriptor_1 = Column(String, nullable=True)
    descriptor_2 = Column(String, nullable=True)
    descriptor_3 = Column(String, nullable=True)
    descriptor_4 = Column(String, nullable=True)
    descriptor_5 = Column(String, nullable=True)
    story_index = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    image_path = Column(String, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Places(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    descriptor_1 = Column(String, nullable=True)
    descriptor_2 = Column(String, nullable=True)
    descriptor_3 = Column(String, nullable=True)
    descriptor_4 = Column(String, nullable=True)
    descriptor_5 = Column(String, nullable=True)
    story_index = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)    
    image_path = Column(String, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    descriptor_1 = Column(String, nullable=True)
    descriptor_2 = Column(String, nullable=True)
    descriptor_3 = Column(String, nullable=True)
    descriptor_4 = Column(String, nullable=True)
    descriptor_5 = Column(String, nullable=True)
    story_index = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)    
    image_path = Column(String, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Threads(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    thread = Column(String, nullable=True)   
    story_index = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)    
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=True)
    type_id = Column(Integer, nullable=True)
    story_index = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))

class ThreadsNotes(Base):
    __tablename__ = "threads_notes"

    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, nullable=True)
    story_index = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST))
    modified_date = Column(DateTime, default=lambda: datetime.now().replace(tzinfo=IST), onupdate=lambda: datetime.now().replace(tzinfo=IST))