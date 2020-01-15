"""Decorators for auth module."""
from functools import wraps

from protocol import make_response

from database import session_scope
from .models import Session


def login_required(func):
    """Check that user is logged in based on the valid token exists in request."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'token' not in request:
            return make_response(request, 401, 'Valid authentication credentials lack')

        with session_scope() as db_session:
            user_session = db_session.query(Session).filter_by(token=request.get('token')).first()
            if not user_session or user_session.closed:
                return make_response(request, 403, 'Access denied')

        return func(request, *args, **kwargs)
    return wrapper
