"""Database connection module for server side messenger app."""
from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import CONNECTION_STRING


engine = create_engine(CONNECTION_STRING)
Base = declarative_base(metadata=MetaData(bind=engine))
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Database connection context manager."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
