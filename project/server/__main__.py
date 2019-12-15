import yaml
import json
from socket import socket
from argparse import ArgumentParser

from protocol import validate_request, make_response
from resolvers import resolve

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024,
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)

host, port = (default_config.get('host'), default_config.get('port'))

try:

    sock = socket()
    sock.bind((host, port,))
    sock.listen(5)

    print(f'Server was started with {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client was connected with {address[0]}:{address[1]}')
        b_request = client.recv(default_config.get('buffersize'))
        request = json.loads(b_request.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    print(f'Controller {action_name} resolved with request {request}')
                    response = controller(request)
                except Exception as error:
                    print(f'Controller {action_name} rejected. Error: {error}')
                    response = make_response(request, 500, 'Internal server error')
            else:
                print(f'Controller {action_name} not found')
                response = make_response(request, 404, f'Action with name {action_name} not supported')
        else:
            print(f'Controller wrong request: {request}')
            response = make_response(request, 400, 'Wrong request format')

        client.send(
            json.dumps(response).encode()
        )

        client.close()

except KeyboardInterrupt:
    print('Server shutdown')
