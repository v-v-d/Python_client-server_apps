"""Middlewares for server side messenger app."""
import zlib
import json
import hmac
from functools import wraps

from protocol import make_response
from auth.models import User
from database import Session


def compression_middleware(func):
    """Decompress request and return compression result."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)
    return wrapper


# def auth_middleware(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         request_obj = json.loads(request)
#         login = request_obj.get('login')
#         token = request_obj.get('token')
#         time = request_obj.get('time')
#
#         session = Session()
#         user = session.query(User).filter_by(name=login).first()
#
#         if user:
#             digest = hmac.new(time, user.password)
#
#             if hmac.compare_digest(digest, token):
#                 return func(request, *args, **kwargs)
#
#         response = make_response(request, 401, 'Access denied')
#         return json.dumps(response).encode()
#     return wrapper
