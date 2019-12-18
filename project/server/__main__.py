import yaml
import json
import logging
from socket import socket
from argparse import ArgumentParser

from handlers import handle_default_request

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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='UTF-8'),
        logging.StreamHandler(),
    ]
)

try:

    sock = socket()
    sock.bind((host, port,))
    sock.listen(5)

    logging.info(f'Server was started with {host}:{port}')

    while True:
        client, address = sock.accept()

        logging.info(f'Client was connected with {address[0]}:{address[1]}')

        b_request = client.recv(default_config.get('buffersize'))

        b_response = handle_default_request(b_request)

        client.send(b_response)

        client.close()

except KeyboardInterrupt:
    logging.info('Server shutdown')
