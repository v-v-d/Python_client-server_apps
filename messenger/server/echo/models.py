from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from auth.models import User    # Нужен для того, чтобы sqlalchemy увидела эту модель в relationship


class Message(Base):
    __tablename__ = 'messages'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True)
    data = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')
