from sqlalchemy import create_engine
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
    """Creates the database and populates specific tables if missing."""
    from .master_tables import StoriesIndex, Characters, Places, Items, Threads
    inspector = inspect(engine)
    
    models = [StoriesIndex, Characters, Places, Items, Threads]  # List all models

    try:
        for model in models:
            if not inspector.has_table(model.__tablename__):  # Check if table exists
                model.__table__.create(engine)  # Create table

                # If it's StoriesIndex, populate indexes 1-5
                if model is StoriesIndex:
                    for i in range(1, 6):  # Ensure index 1 to 5 is created
                        story = StoriesIndex(index=i, name=None, description=None)
                        session.add(story)
                    session.commit()
    except IntegrityError:
        session.rollback()
    finally:
        session.close()
