import yaml
import logging

from threading import Thread
from select import select
from socket import socket
from argparse import ArgumentParser

from handlers import handle_default_request


class TypedProperty:
    def __init__(self, name, type_name, default=None):
        self.name = f'_{name}'
        self.type = type_name
        self.default = default if default else type_name()

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f'Value must be str type {self.type}')
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError('Unable to delete attribute')


class ConfigFromCLI:
    def __init__(self):
        self._host = '127.0.0.1'
        self._port = 8000
        self._set_config()

    def _set_config(self):
        config = self._get_config_from_file()
        if config:
            self._host = config.get('host')
            self._port = int(config.get('port'))

    def _get_config_from_file(self):
        args = self._get_args()
        if args.config:
            with open(args.config) as file:
                return yaml.load(file, Loader=yaml.Loader)

    @staticmethod
    def _get_args():
        parser = ArgumentParser()
        parser.add_argument(
            '-c', '--config', type=str,
            required=False, help='Sets config file path'
        )
        return parser.parse_args()

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port


class Server:
    def __init__(self, buffersize=1024):
        self.buffersize = buffersize
        self.host = TypedProperty('host', str, '127.0.0.1')
        self.port = TypedProperty('port', int, 8000)
        self._socket = socket()
        self._requests = []
        self._connections = []
        self._r_list = []
        self._w_list = []
        self._x_list = []

    def run(self):
        try:
            self._init_session()
            while True:
                self._accept_client()
                self._handle_clients()
                self._read()
                self._write()
        except KeyboardInterrupt:
            logging.info('Server shutdown')

    def _init_session(self):
        self._socket.bind((self.host, self.port, ))
        # docks.python.org: Empty sequences are allowed, but acceptance of three empty sequences is platform-dependent.
        # (It is known to work on Unix but not on Windows.)
        # Для винды устанавливаем таймаут, чтобы завелся select(). С пустым списком self._connections будет
        # OSError: [WinError 10022] An invalid argument was supplied. При этом надо успеть за этот таймаут подключиться
        # клиентом к серверу. Этот костыль онли для отладки на винде
        # В боевом режиме устанавливаем таймаут в 0
        # self._socket.settimeout(0)
        self._socket.settimeout(2)
        self._socket.listen(5)
        logging.info(f'Server was started with {self.host}:{self.port}')

    def _accept_client(self):
        try:
            client, address = self._socket.accept()
            self._connections.append(client)
            logging.info(f'Client was connected with {address[0]}:{address[1]} | connections: {self._connections}')
        except Exception:
            pass

    def _handle_clients(self):
        self._r_list, self._w_list, self._x_list = select(
            self._connections, self._connections, self._connections, 0
        )

    def _read(self):
        for client in self._r_list:
            Thread(target=self._read_by_single_thread, args=(client, )).start()

    def _read_by_single_thread(self, client):
        try:
            bytes_request = self._get_request(client)
        except Exception:
            self._remove_client(client)
        else:
            if bytes_request:
                self._add_request(bytes_request)

    def _get_request(self, client):
        return client.recv(self.buffersize)

    def _remove_client(self, client):
        self._connections.remove(client)

    def _add_request(self, request):
        self._requests.append(request)

    def _write(self):
        if self._requests:
            for client in self._w_list:
                Thread(target=self._write_by_single_thread, args=(client, )).start()

    def _write_by_single_thread(self, client):
        try:
            client.send(self._handle_request())
        except Exception:
            self._remove_client(client)

    def _handle_request(self):
        return handle_default_request(self._get_last_request())

    def _get_last_request(self):
        return self._requests.pop()


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='UTF-8'),
        logging.StreamHandler(),
    ]
)


if __name__ == '__main__':
    config = ConfigFromCLI()

    server = Server()
    server.host, server.port = config.host, config.port
    server.run()

# def read(sock, connections, requests, buffersize):
#     try:
#         bytes_request = sock.recv(buffersize)
#     except Exception:
#         connections.remove(sock)
#     else:
#         if bytes_request:
#             requests.append(bytes_request)
#
#
# def write(sock, connections, response):
#     try:
#         sock.send(response)
#     except Exception:
#         connections.remove(sock)
#
#
# parser = ArgumentParser()
#
# parser.add_argument(
#     '-c', '--config', type=str,
#     required=False, help='Sets config file path'
# )
#
# args = parser.parse_args()
#
# default_config = {
#     'host': 'localhost',
#     'port': 8000,
#     'buffersize': 1024,
# }
#
# if args.config:
#     with open(args.config) as file:
#         file_config = yaml.load(file, Loader=yaml.Loader)
#         default_config.update(file_config)
#
# host, port = (default_config.get('host'), default_config.get('port'))
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('main.log', encoding='UTF-8'),
#         logging.StreamHandler(),
#     ]
# )
#
# requests = []
# connections = []
#
# try:
#
#     sock = socket()
#     sock.bind((host, port,))
#     # docks.python.org: Empty sequences are allowed, but acceptance of three empty sequences is platform-dependent.
#     # (It is known to work on Unix but not on Windows.)
#     # Для винды устанавливаем таймаут, чтобы завелся select.select(). С пустым списком connections будет
#     # OSError: [WinError 10022] An invalid argument was supplied. При этом надо успеть за этот таймаут подключиться
#     # клиентом к серверу. Этот костыль онли для отладки на винде
#     # В боевом режиме устанавливаем таймаут в 0
#     # sock.settimeout(0)
#     sock.settimeout(2)
#     sock.listen(5)
#
#     logging.info(f'Server was started with {host}:{port}')
#
#     while True:
#         try:
#             client, address = sock.accept()
#
#             connections.append(client)
#
#             logging.info(f'Client was connected with {address[0]}:{address[1]} | connections: {connections}')
#         except:
#             pass
#
#         r_list, w_list, x_list = select.select(
#             connections, connections, connections, 0
#         )
#
#         for r_client in r_list:
#             r_thread = threading.Thread(
#                 target=read, args=(r_client, connections, requests, default_config.get('buffersize'))
#             )
#             r_thread.start()
#
#         if requests:
#             b_request = requests.pop()
#             b_response = handle_default_request(b_request)
#
#             for w_client in w_list:
#                 w_thread = threading.Thread(
#                     target=write, args=(w_client, connections, b_response)
#                 )
#                 w_thread.start()
#
# except KeyboardInterrupt:
#     logging.info('Server shutdown')
