from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///default.db')

metadata = MetaData(bind=engine)

Base = declarative_base(metadata=metadata)

Session = sessionmaker(bind=engine)
