import zlib
import yaml
import json
import hashlib
from threading import Thread
from socket import socket
from datetime import datetime
from argparse import ArgumentParser


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


class Client:
    def __init__(self, buffersize=1024):
        self.buffersize = buffersize
        self.host = TypedProperty('host', str, '127.0.0.1')
        self.port = TypedProperty('port', int, 8000)
        self._socket = socket()

    def run(self):
        self._connect()
        try:
            self._read()
            self._write()
        except KeyboardInterrupt:
            self._disconnect()

    def _connect(self):
        self._socket.connect((self.host, self.port))
        print(f'Client was started with {self.host}:{self.port}')

    def _read(self):
        Thread(target=self._read_by_single_thread).start()

    def _read_by_single_thread(self):
        while True:
            print(f'Client got response: {self._get_b_response().decode()}')

    def _get_b_response(self):
        return zlib.decompress(self._get_compressed_response())

    def _get_compressed_response(self):
        return self._socket.recv(self.buffersize)

    def _write(self):
        while True:
            self._send_request()

    def _send_request(self):
        self._socket.send(self._get_compressed_b_request())
        print(f'Client send request')

    def _get_compressed_b_request(self):
        return zlib.compress(self._get_s_request().encode())

    def _get_s_request(self):
        return json.dumps(self._get_request())

    def _get_request(self):
        return {
            'action': input('Enter action: '),
            'time': datetime.now().timestamp(),
            'data': input('Enter data: '),
            'token': self._get_token(),
        }

    @staticmethod
    def _get_token():
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )
        return hash_obj.hexdigest()

    def _disconnect(self):
        self._socket.close()
        print('Client shutdown')


if __name__ == '__main__':
    config = ConfigFromCLI()

    client = Client()
    client.host, client.port = config.host, config.port
    client.run()

# def read(sock, buffersize):
#     while True:
#         compressed_response = sock.recv(buffersize)
#         b_response = zlib.decompress(compressed_response)
#         print(f'Client got response: {b_response.decode()}')
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
# sock = socket()
# sock.connect(
#     (default_config.get('host'), default_config.get('port'))
# )
#
# print('Client was started')
#
# try:
#     read_thread = Thread(target=read, args=(sock, default_config.get('buffersize')))
#     read_thread.start()
#
#     while True:
#         hash_obj = hashlib.sha256()
#         hash_obj.update(
#             str(datetime.now().timestamp()).encode()
#         )
#
#         action = input('Enter action: ')
#         data = input('Enter data: ')
#
#         request = {
#             'action': action,
#             'time': datetime.now().timestamp(),
#             'data': data,
#             'token': hash_obj.hexdigest(),
#         }
#
#         s_request = json.dumps(request)
#         b_request = zlib.compress(s_request.encode())
#         sock.send(b_request)
#         print(f'Client send request: {s_request}')
# except KeyboardInterrupt:
#     sock.close()
#     print('Client shutdown')
