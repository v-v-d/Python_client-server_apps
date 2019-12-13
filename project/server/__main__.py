import yaml
from socket import socket
from argparse import ArgumentParser

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
        print(f'Client send message: {b_request.decode()}')
        client.send(b_request)
        client.close()

except KeyboardInterrupt:
    print('Server shutdown')
