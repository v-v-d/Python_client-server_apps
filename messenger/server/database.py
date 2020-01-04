from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import CONNECTION_STRING


engine = create_engine(CONNECTION_STRING)
Base = declarative_base(metadata=MetaData(bind=engine))
Session = sessionmaker(bind=engine)
