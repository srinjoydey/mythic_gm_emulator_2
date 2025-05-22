from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect



DATABASE_URL = "sqlite:///mythic_stories.db"
# engine = create_engine(DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()  # Defined centrally

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

session = SessionLocal()


def initialize_db():
    """Creates the database and populates the table if missing."""
    from .master_tables import StoriesIndex
    inspector = inspect(engine)
    
    if not inspector.has_table("stories_index"):  # Check if table exists
        StoriesIndex.__table__.create(engine)  # Create table
        
        # ✅ Insert five rows with predefined indexes

        try:
            for i in range(1, 6):  # Ensure index 1 to 5 is created
                story = StoriesIndex(index=i, name=None, description=None)
                session.add(story)
            session.commit()
        except IntegrityError:
            session.rollback()
        finally:
            session.close()