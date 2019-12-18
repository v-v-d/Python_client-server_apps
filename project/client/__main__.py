import zlib
import yaml
import json
import hashlib
import logging
from socket import socket
from datetime import datetime
from argparse import ArgumentParser


def write(sock):
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
    logging.info(f'Client send request: {s_request}')


def read(sock):
    compressed_response = sock.recv(default_config.get('buffersize'))

    b_response = zlib.decompress(compressed_response)

    logging.info(f'Client got response: {b_response.decode()}')


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)
parser.add_argument(
    '-m', '--mode', type=str, default='r',
    required=False, help='Sets client mode'
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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('client.log', encoding='UTF-8'),
        logging.StreamHandler(),
    ]
)


sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'))
)

logging.info('Client was started')

try:
    while True:
        if args.mode == 'w':
            write(sock)

        elif args.mode == 'r':
            read(sock)
except KeyboardInterrupt:
    sock.close()
    print('Client shutdown')
