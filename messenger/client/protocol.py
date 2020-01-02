from datetime import datetime


def make_request(action, data, token):
    return {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
        'token': token
    }
