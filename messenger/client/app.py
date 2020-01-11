import sys
import zlib
import json
import hashlib
import logging
from threading import Thread
from socket import socket
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from protocol import make_request
from utils import get_chunk


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
        logging.info(message, exc_info=exc_val)
        self._socket.close()
        return True

    def run(self):
        self._connect()
        while True:
            self._read()
            self._write()
        # self._read()
        #
        # app = QApplication(sys.argv)
        #
        # self._render()
        #
        # sys.exit(app.exec_())

    def _connect(self):
        self._socket.connect((self.host, self.port))
        logging.info(f'Client was started with {self.host}:{self.port}')

    def _read(self):
        Thread(target=self._read_by_single_thread).start()

    def _read_by_single_thread(self):
        logging.info(f'Client got response: {self._get_decrypted_response()}')

    def _get_decrypted_response(self):
        encrypted_response = self._get_encrypted_response()
        nonce, encrypted_response = get_chunk(encrypted_response, 16)
        key, encrypted_response = get_chunk(encrypted_response, 16)
        tag, encrypted_response = get_chunk(encrypted_response, 16)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        return cipher.decrypt_and_verify(encrypted_response, tag).decode()

    def _get_encrypted_response(self):
        return zlib.decompress(self._get_compressed_b_response())

    def _get_compressed_b_response(self):
        return self._socket.recv(self.buffersize)

    @staticmethod
    def _render():
        window = QMainWindow()
        window.show()

    def _write(self):
        self._socket.send(self._get_compressed_b_request())
        logging.info(f'Client send request')

    def _get_compressed_b_request(self):
        return zlib.compress(self._get_encrypted_b_request())

    def _get_encrypted_b_request(self):
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_request, tag = cipher.encrypt_and_digest(self._get_b_request())
        return b'%(nonce)s%(key)s%(tag)s%(data)s' % {
            b'nonce': cipher.nonce, b'key': key, b'tag': tag, b'data': encrypted_request
        }

    def _get_b_request(self):
        return json.dumps(self._get_request()).encode()

    def _get_request(self):
        action = input('Enter action: ')
        data = input('Enter data: ')
        return make_request(action, data, self._get_token())

    @staticmethod
    def _get_token():
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )
        return hash_obj.hexdigest()
