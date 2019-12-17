import yaml
import json
import hashlib
import logging
from socket import socket
from datetime import datetime
from argparse import ArgumentParser

import client_log_config

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

logger = logging.getLogger('client')

sock = socket()
sock.connect(
    (default_config.get('host'), default_config.get('port'))
)

logger.info('Client was started')

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

sock.send(s_request.encode())
logger.info(f'Client send request: {s_request}')
b_response = sock.recv(default_config.get('buffersize'))
logger.info(f'Client got response: {b_response.decode()}')
