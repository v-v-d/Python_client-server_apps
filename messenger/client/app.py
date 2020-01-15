"""Main class based logic for client app."""
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
    """Control the value type for an attribute and prevent removing an attribute from an instance of an object."""
    def __init__(self, name, type_name, default=None):
        self.name = f'_{name}'
        self.type = type_name
        self.default = default if default else type_name()

    def __get__(self, instance, cls):
        """Return the attribute value by using '.' from an instance of an object."""
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        """Set attribute value with default type."""
        if not isinstance(value, self.type):
            raise TypeError(f'Value must be str type {self.type}')
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        """Prevent removing an attribute from an instance of an object."""
        raise AttributeError('Unable to delete attribute')


class Application:
    """Messenger client side main logic."""
    def __init__(self, buffersize=1024):
        self.buffersize = buffersize
        self.host = TypedProperty('host', str, '127.0.0.1')
        self.port = TypedProperty('port', int, 8000)
        self._socket = None

    def __enter__(self):
        """Set up socket when enter by 'with' context manager."""
        if not self._socket:
            self._socket = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log the message and ignore exception when exit by 'with' context manager."""
        message = 'Client shutdown'
        if exc_type:
            if exc_type is not KeyboardInterrupt:
                message = 'Client stopped with error'
        logging.info(message, exc_info=exc_val)
        self._socket.close()
        return True

    def run(self):
        """Run the client."""
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
        """Connect to server with host and port attributes."""
        self._socket.connect((self.host, self.port))
        logging.info(f'Client was started with {self.host}:{self.port}')

    def _read(self):
        """Start reading response thread."""
        Thread(target=self._read_by_single_thread).start()

    def _read_by_single_thread(self):
        """Logging the reading response."""
        logging.info(f'Client got response: {self._get_decrypted_response()}')

    def _get_decrypted_response(self):
        """Get decrypted response with Crypto module and decode it."""
        encrypted_response = self._get_encrypted_response()
        nonce, encrypted_response = get_chunk(encrypted_response, 16)
        key, encrypted_response = get_chunk(encrypted_response, 16)
        tag, encrypted_response = get_chunk(encrypted_response, 16)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        return cipher.decrypt_and_verify(encrypted_response, tag).decode()

    def _get_encrypted_response(self):
        """Get encrypted bytes response."""
        return zlib.decompress(self._get_compressed_b_response())

    def _get_compressed_b_response(self):
        """Get compressed bytes response."""
        return self._socket.recv(self.buffersize)

    @staticmethod
    def _render():
        """Show GUI window."""
        window = QMainWindow()
        window.show()

    def _write(self):
        """Send compressed bytes request to server."""
        self._socket.send(self._get_compressed_b_request())
        logging.info(f'Client send request')

    def _get_compressed_b_request(self):
        """Get compressed bytes request."""
        return zlib.compress(self._get_encrypted_b_request())

    def _get_encrypted_b_request(self):
        """Get encrypted bytes request with Crypto module."""
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_request, tag = cipher.encrypt_and_digest(self._get_b_request())
        return b'%(nonce)s%(key)s%(tag)s%(data)s' % {
            b'nonce': cipher.nonce, b'key': key, b'tag': tag, b'data': encrypted_request
        }

    def _get_b_request(self):
        """Dump request to JSON and turn it to bytes."""
        return json.dumps(self._get_request()).encode()

    def _get_request(self):
        """Get request from client via inputs."""
        action = input('Enter action: ')
        data = json.loads(input('Enter data: '))
        return make_request(action, data, self._get_token())

    @staticmethod
    def _get_token():
        """Get token via hashlib and timestamp."""
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )
        return hash_obj.hexdigest()
