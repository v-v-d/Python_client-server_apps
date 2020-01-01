from sqlalchemy import (
    create_engine, Table, String,
    Integer, MetaData, Column, ForeignKey
    )
from sqlalchemy.orm import mapper


engine = create_engine('sqlite:///messenger.db')

metadata = MetaData()

serverdate_requests = Table(
    'serverdate_requests', metadata,
    Column('id', Integer, primary_key=True),
    # Column('user_id', Integer, ForeignKey('users.id')),
    Column('response_id', Integer, ForeignKey('echo_responses.id')),
    Column('time', String),
    Column('data', String),
    Column('token', String),
)

serverdate_responses = Table(
    'serverdate_responses', metadata,
    Column('id', Integer, primary_key=True),
    # Column('user_id', Integer, ForeignKey('users.id')),
    Column('request_id', Integer, ForeignKey('echo_requests.id')),
    Column('time', String),
    Column('data', String),
    Column('code', Integer),
)

metadata.create_all(engine)


class ServerdateRequests:
    # def __init__(self, user_id, response_id, time, data, token):
    #     self.user_id = user_id
    def __init__(self, response_id, time, data, token):
        self.response_id = response_id
        self.time = time
        self.data = data
        self.token = token


class ServerdateResponses:
    # def __init__(self, user_id, request_id, time, data, code):
    #     self.user_id = user_id
    def __init__(self, request_id, time, data, code):
        self.request_id = request_id
        self.time = time
        self.data = data
        self.code = code


mapper(ServerdateRequests, serverdate_requests)
mapper(ServerdateResponses, serverdate_responses)

ServerdateRequests(1, '1576601472.797791', 'asd', '47a73f5c1abe64053477fbd3b1ec21e9632ec03e6193992b240b8d245003e61c')
ServerdateResponses(1, '1576601472.797791', 'asd', 200)
#
# EchoRequests(1, 1, '1576601472.797791', 'asd', '47a73f5c1abe64053477fbd3b1ec21e9632ec03e6193992b240b8d245003e61c')
# EchoResponses(1, 1, '1576601472.797791', 'asd', 200)
