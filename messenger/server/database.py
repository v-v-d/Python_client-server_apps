from sqlalchemy import MetaData
from sqlalchemy import create_engine


engine = create_engine('sqlite:///default.db')

database_metadata = MetaData()
