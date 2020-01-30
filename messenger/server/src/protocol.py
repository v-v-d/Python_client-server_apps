"""Protocol for server side messenger app."""


def validate_request(raw):
    """Checking for exists of 'action' and 'time' in request."""
    return True if 'action' in raw and 'time' in raw else False


def make_response(request, code, data=None):
    """Make response based on passed request, status code and data."""
    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code,
    }
