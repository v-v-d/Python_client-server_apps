from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, Integer, DateTime, String

from database import database_metadata


message_table = Table(
    'messages', database_metadata,
    Column('id', Integer, primary_key=True),
    Column('content', String),
    Column('user', String),
    Column('created', DateTime)
)


class Message:
    def __init__(self, content, user, date):
        self.content = content
        self.user = user
        self.date = date


mapper(Message, message_table)
