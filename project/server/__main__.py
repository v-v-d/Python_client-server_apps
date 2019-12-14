import yaml
import json
from socket import socket
from argparse import ArgumentParser

from project.server.protocol import validate_request, make_response

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
            action = request.get('action')
            data = request.get('data')

            if action == 'echo':
                try:
                    print(f'Client send message: {data}')
                    response = make_response(request, 200, data)
                except Exception as error:
                    response = make_response(request, 500, 'Internal server error')
            else:
                response = make_response(request, 404, f'Action with name {action} not supported')
        else:
            response = make_response(request, 400, 'Wrong request format')

        client.send(
            json.dumps(response).encode()
        )

        client.close()

except KeyboardInterrupt:
    print('Server shutdown')
