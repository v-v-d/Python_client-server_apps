import zlib
import yaml
import json
import hashlib
import threading
from socket import socket
from datetime import datetime
from argparse import ArgumentParser


def read(sock, buffersize):
    while True:
        compressed_response = sock.recv(buffersize)
        b_response = zlib.decompress(compressed_response)
        print(f'Client got response: {b_response.decode()}')


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

sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'))
)

print('Client was started')

try:
    read_thread = threading.Thread(
        target=read, args=(sock, default_config.get('buffersize'))
    )
    read_thread.start()

    while True:
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = input('Enter action: ')
        data = input('Enter data: ')

        request = {
            'action': action,
            'time': datetime.now().timestamp(),
            'data': data,
            'token': hash_obj.hexdigest(),
        }

        s_request = json.dumps(request)
        b_request = zlib.compress(s_request.encode())
        sock.send(b_request)
        print(f'Client send request: {s_request}')
except KeyboardInterrupt:
    sock.close()
    print('Client shutdown')
