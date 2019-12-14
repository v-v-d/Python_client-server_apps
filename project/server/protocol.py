def validate_request(raw):
    return True if 'action' in raw and 'time' in raw else False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code,
    }
