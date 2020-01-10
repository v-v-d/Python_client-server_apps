import zlib
import json
import hmac
from functools import wraps
from Crypto.Cipher import AES

from protocol import make_response
from auth.models import User
from database import Session


def compression_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)
    return wrapper


def encryption_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        encrypted_request = json.loads(request)
        key = encrypted_request.get('key')
        data = encrypted_request.get('data')
        cypher = AES.new(key, AES.MODE_CDC)
        decrypted_data = cypher.decrypt(data)
        decrypted_request = encrypted_request.copy()
        decrypted_request['data'] = decrypted_data
        b_request = json.dumps(decrypted_request).encode()

        b_response = func(b_request, *args, **kwargs)

        decrypted_response = json.loads(b_response)
        decrypted_data = decrypted_response.get('data')
        encrypted_data = cypher.encrypt(decrypted_data)
        encrypted_response = decrypted_response.copy()
        encrypted_response['data'] = encrypted_data
        return json.dumps(encrypted_response).encode()
    return wrapper


def auth_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        request_obj = json.loads(request)
        login = request_obj.get('login')
        token = request_obj.get('token')
        time = request_obj.get('time')

        session = Session()
        user = session.query(User).filter_by(name=login).first()

        if user:
            digest = hmac.new(time, user.password)

            if hmac.compare_digest(digest, token):
                return func(request, *args, **kwargs)

        response = make_response(request, 401, 'Access denied')
        return json.dumps(response).encode()
    return wrapper


# def decrypt_request_data(request):
#     encrypted_request = get_encrypted_request(request)
#     data = encrypted_request.get('data')
#     decrypted_data = get_cypher(request).decrypt(data)
#     decrypted_request = encrypted_request.copy()
#     decrypted_request['data'] = decrypted_data
#     return json.dumps(decrypted_request).encode()
#
#
# def encrypt_b_response_data(b_response, request):
#     decrypted_response = json.loads(b_response)
#     decrypted_data = decrypted_response.get('data')
#     encrypted_data = get_cypher(request).encrypt(decrypted_data)
#     encrypted_response = decrypted_response.copy()
#     encrypted_response['data'] = encrypted_data
#     return encrypted_response
#
#
# def get_cypher(request):
#     return AES.new(get_encrypted_request(request).get('key'), AES.MODE_CDC)
#
#
# def get_encrypted_request(request):
#     return json.loads(request)
