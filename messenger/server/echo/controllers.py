from protocol import make_response
from database import Session
from decorators import logged

from .models import Message


@logged
def echo_controller(request):
    data = request.get('data')
    session = Session()
    message = Message(data=data.get('text'))
    # message = Message(data=data)
    session.add(message)
    session.commit()
    session.close()
    return make_response(request, 200, data)


@logged
def update_message_controller(request):
    message_data = request.get('data')
    message_id = request.get('message_id')
    session = Session()
    message = session.query(Message).filter_by(id=message_id).first()
    message.data = message_data
    session.commit()
    session.close()
    return make_response(request, 200)


@logged
def delete_message_controller(request):
    message_id = request.get('message_id')
    session = Session()
    message = session.query(Message).filter_by(id=message_id).first()
    session.delete(message)
    session.commit()
    session.close()
    return make_response(request, 200)


@logged
def get_messages_controller(request):
    session = Session()
    messages = [{'data': item.data, 'created': item.created.timestamp()} for item in session.query(Message).all()]
    return make_response(request, 200, messages)

# TODO: Реализовать контроллеры через session_scope()
