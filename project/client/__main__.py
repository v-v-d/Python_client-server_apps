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
sock.connect((host, port,))

print('Client was started')

data = input('Enter data: ')

sock.send(data.encode())
print(f'Client send data: {data}')
b_response = sock.recv(1024)
print(b_response.decode())
