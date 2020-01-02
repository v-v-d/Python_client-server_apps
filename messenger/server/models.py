from sqlalchemy import (
    create_engine, Table, String,
    Integer, MetaData, Column, ForeignKey
    )
from sqlalchemy.orm import mapper


engine = create_engine('sqlite:///messenger.db')

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
    Column('password', String),
)

client_history = Table(
    'client_history', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('entry_time', String),
    Column('ip_address', String),
)

contact_list = Table(
    'contact_list', metadata,
    Column('id', Integer, primary_key=True),
    Column('from_user_id', Integer, ForeignKey('users.id')),
    Column('to_user_id', Integer, ForeignKey('users.id')),
)

metadata.create_all(engine)


class Users:
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password


class ClientHistory:
    def __init__(self, user_id, entry_time, ip_address):
        self.user_id = user_id
        self.entry_time = entry_time
        self.ip_address = ip_address


class ContactList:
    def __init__(self, from_user_id, to_user_id):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id


mapper(Users, users)
mapper(ClientHistory, client_history)
mapper(ContactList, contact_list)

Users('Homer', 'Homer Simpson', 'qwerty123')
ClientHistory(1, '1576601472.797791', '168.63.129.16')
ContactList(1, 2)
