"""Middlewares for server side messenger app."""
import zlib

from functools import wraps


def compression_middleware(func):
    """Decompress request and return compression result."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)
    return wrapper
