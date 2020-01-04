from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String

from database import Base


class Message(Base):
    __tablename__ = 'messages'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True)
    data = Column(String)
    created = Column(DateTime, default=datetime.now())

    def __init__(self, data, created):
        self.data = data
        self.created = created
