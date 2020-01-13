from protocol import make_response
from database import Session, session_scope
from decorators import logged

from .models import Message


@logged
def echo_controller(request):
    data = request.get('data')
    with session_scope() as session:
        message = Message(data=data.get('text'))
        session.add(message)
    return make_response(request, 200, data)


@logged
def update_message_controller(request):
    data = request.get('data')
    message_data = data.get('text')
    message_id = data.get('message_id')
    with session_scope() as session:
        message = session.query(Message).filter_by(id=message_id).first()
        message.data = message_data
    return make_response(request, 200)


@logged
def delete_message_controller(request):
    data = request.get('data')
    message_id = data.get('message_id')
    with session_scope() as session:
        message = session.query(Message).filter_by(id=message_id).first()
        session.delete(message)
    return make_response(request, 200)


@logged
def get_messages_controller(request):
    with session_scope() as session:
        messages = [{'data': item.data, 'created': item.created.timestamp()} for item in session.query(Message).all()]
    return make_response(request, 200, messages)
