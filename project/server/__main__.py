import yaml
from socket import socket
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

host = 'localhost'
port = 8000

if args.config:
    with open(args.config) as file:
        config = yaml.load(file, Loader=yaml.Loader)
        host = config.get('host', host)
        port = config.get('port', port)

sock = socket()
sock.bind((host, port,))
sock.listen(5)

print(f'Server was started with {host}:{port}')

while True:
    client, address = sock.accept()
    print(f'Client was connected with {address[0]}:{address[1]}')
    b_request = client.recv(1024)
    print(f'Client send message: {b_request.decode()}')
    client.send(b_request)
    client.close()
