from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
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
