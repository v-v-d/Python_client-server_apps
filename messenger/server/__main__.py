import yaml
import select
import logging
import threading
from socket import socket
from argparse import ArgumentParser

from handlers import handle_default_request


def read(sock, connections, requests, buffersize):
    try:
        bytes_request = sock.recv(buffersize)
    except Exception:
        connections.remove(sock)
    else:
        if bytes_request:
            requests.append(bytes_request)


def write(sock, connections, response):
    try:
        sock.send(response)
    except Exception:
        connections.remove(sock)


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

requests = []
connections = []

try:

    sock = socket()
    sock.bind((host, port,))
    # Для винды устанавливаем таймаут, чтобы завелся select.select(). С пустым списком connections будет
    # OSError: [WinError 10022] An invalid argument was supplied. При этом надо успеть за этот таймаут подключиться
    # клиентом к серверу. Этот костыль онли для отладки на винде
    sock.settimeout(2)
    # В боевом режиме устанавливаем таймаут в 0
    # sock.settimeout(0)
    sock.listen(5)

    logging.info(f'Server was started with {host}:{port}')

    while True:
        try:
            client, address = sock.accept()

            connections.append(client)

            logging.info(f'Client was connected with {address[0]}:{address[1]} | connections: {connections}')
        except:
            pass

        r_list, w_list, x_list = select.select(
            connections, connections, connections, 0
        )

        for r_client in r_list:
            r_thread = threading.Thread(
                target=read, args=(r_client, connections, requests, default_config.get('buffersize'))
            )
            r_thread.start()

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in w_list:
                w_thread = threading.Thread(
                    target=write, args=(w_client, connections, b_response)
                )
                w_thread.start()

except KeyboardInterrupt:
    logging.info('Server shutdown')
