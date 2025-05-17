from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()  # Defined centrally

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)