"""Protocol for client side messenger app."""
from datetime import datetime


def make_request(action, data, token):
    """Make request based on passed arguments and timestamp."""
    return {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
        'token': token
    }
