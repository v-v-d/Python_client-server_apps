"""Handlers for server side messenger application."""
import json
import logging

from src.resolvers import resolve
from src.protocol import validate_request, make_response
from src.middlewares import compression_middleware
from src.security import encryption_middleware


@compression_middleware
@encryption_middleware
def handle_default_request(raw_request):
    """Make response based on request."""
    request = json.loads(raw_request.decode())

    if validate_request(request):
        action_name = request.get('action')
        controller = resolve(action_name)
        if controller:
            try:
                logging.debug(f'Controller {action_name} resolved with request {request}')
                response = controller(request)
            except Exception as error:
                logging.critical(f'Controller {action_name} rejected. Error: {error}')
                response = make_response(request, 500, 'Internal server error')
        else:
            logging.error(f'Controller {action_name} not found')
            response = make_response(request, 404, f'Action with name {action_name} not supported')
    else:
        logging.error(f'Controller wrong request: {request}')
        response = make_response(request, 400, 'Wrong request format')

    return json.dumps(response).encode()
