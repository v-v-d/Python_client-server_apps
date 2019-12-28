import zlib
import yaml
import json
import hashlib
from threading import Thread
from socket import socket
from datetime import datetime
from argparse import ArgumentParser


class ClientConfig:
    def __init__(self):
        self._config_kwargs = {'host': '127.0.0.1', 'port': 8000}
        self.set_config_kwargs()  # TODO: Сделать проверку на валидность

    @staticmethod
    def get_config_file():
        parser = ArgumentParser()
        parser.add_argument(
            '-c', '--config', type=str,
            required=False, help='Sets config file path'
        )
        return parser.parse_args()

    def get_kwargs_from_file(self):
        config_file = self.get_config_file()
        if config_file.config:
            with open(config_file.config) as file:
                config_file = yaml.load(file, Loader=yaml.Loader)
                return config_file

    def set_config_kwargs(self):
        config_kwargs = self.get_kwargs_from_file()
        if config_kwargs:
            self._config_kwargs = config_kwargs

    @property
    def config_kwargs(self):
        return self._config_kwargs


class Client:
    def __init__(self, buffersize=1024):
        self.buffersize = buffersize
        self._host = ClientConfig().config_kwargs.get('host', '127.0.0.1')  # TODO: Сделать проверку на валидность
        self._port = ClientConfig().config_kwargs.get('port', 8000)  # TODO: Сделать проверку на валидность
        self._socket = socket()

    def start_session(self):
        self._connect()
        try:
            self._read()
            self._write()
        except KeyboardInterrupt:
            self._disconnect()

    def _connect(self):
        self._socket.connect((self._host, self._port))
        print('Client was started')

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
    client = Client()
    client.start_session()

    # TODO: Добавить дескриптор атрибутов для класса Client

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
