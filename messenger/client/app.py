import sys
import zlib
import json
import hashlib
import logging
from threading import Thread
from socket import socket
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow

from protocol import make_request


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


class Application:
    def __init__(self, buffersize=1024):
        self.buffersize = buffersize
        self.host = TypedProperty('host', str, '127.0.0.1')
        self.port = TypedProperty('port', int, 8000)
        self._socket = None

    # Методы __enter__ и __exit__ для работы с контекстным менеджером 'with'
    def __enter__(self):
        if not self._socket:
            self._socket = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shutdown'
        if exc_type:
            if exc_type is not KeyboardInterrupt:
                message = 'Client stopped with error'
        logging.info(message)
        self._socket.close()
        return True

    def run(self):
        self._connect()
        self._read()

        app = QApplication(sys.argv)

        self._render()

        sys.exit(app._exec())

        # while True:
        #     self._read()
        #     self._write()

    def _connect(self):
        self._socket.connect((self.host, self.port))
        logging.info(f'Client was started with {self.host}:{self.port}')

    def _read(self):
        Thread(target=self._read_by_single_thread).start()

    def _read_by_single_thread(self):
        logging.info(f'Client got response: {self._get_response()}')

    def _get_response(self):
        return zlib.decompress(self._get_compressed_b_response()).decode()

    def _get_compressed_b_response(self):
        return self._socket.recv(self.buffersize)

    def _render(self):
        window = QMainWindow()
        window.show()

    # def _write(self):
    #     self._socket.send(self._get_compressed_b_request())
    #     logging.info(f'Client send request')
    #
    # def _get_compressed_b_request(self):
    #     return zlib.compress(self._get_s_request().encode())
    #
    # def _get_s_request(self):
    #     return json.dumps(self._get_request())
    #
    # def _get_request(self):
    #     action = input('Enter action: ')
    #     data = input('Enter data: ')
    #     return make_request(action, data, self._get_token())
    #
    # @staticmethod
    # def _get_token():
    #     hash_obj = hashlib.sha256()
    #     hash_obj.update(
    #         str(datetime.now().timestamp()).encode()
    #     )
    #     return hash_obj.hexdigest()
