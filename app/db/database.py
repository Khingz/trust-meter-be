"""Database module"""

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from app.utils.settings import settings
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(settings.DB_URL);
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()

