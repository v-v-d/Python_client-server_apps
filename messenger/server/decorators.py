"""Decorators for server side messenger app."""
import logging
from functools import wraps


logger = logging.getLogger('decorators')


def logged(func):
    """Logging name of controller and passed request."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{func.__name__}: {request}')
        return func(request, *args, **kwargs)
    return wrapper
