import hmac
from datetime import datetime

from database import session_scope
from protocol import make_response

from .decorators import login_required
from .utils import authenticate, login
from .settings import SECRET_KEY
from .models import User, Session


def login_controller(request):
    data = request.get('data')
    errors = _get_validation_errors(request, 'time')
    errors.update(_get_validation_errors(data, 'password', 'login'))
    if errors:
        return make_response(request, 400, {'errors': errors})

    user = authenticate(data.get('login'), data.get('password'))
    if user:
        token = login(request, user)
        return make_response(request, 200, {'token': token})

    return make_response(request, 400, 'Enter correct login or password')


def registration_controller(request):
    data = request.get('data')
    errors = _get_validation_errors(data, 'password', 'login')
    if errors:
        return make_response(request, 400, {'errors': errors})

    hmac_obj = hmac.new(SECRET_KEY.encode(), data.get('password').encode())
    password_digest = hmac_obj.hexdigest()

    with session_scope() as db_session:
        user = User(name=data.get('login'), password=password_digest)
        db_session.add(user)
    token = login(request, user)
    return make_response(request, 200, {'token': token})


def _get_validation_errors(request, *attributes):
    errors = {}
    [errors.update({attribute: 'Attribute is required'}) for attribute in attributes if attribute not in request]
    return errors


@login_required
def logout_controller(request):
    with session_scope() as db_session:
        user_session = db_session.query(Session).filter_by(token=request.get('token')).first()
        user_session.closed = datetime.now()
        return make_response(request, 200, 'Session closed')
