import logging
from threading import Thread
from select import select
from socket import socket


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
    def __init__(self, handler, clients_qty=5, buffersize=1024):
        self.handler = handler
        self.buffersize = buffersize
        self.clients_qty = clients_qty
        self.host = TypedProperty('host', str, '127.0.0.1')
        self.port = TypedProperty('port', int, 8000)
        self._socket = None
        self._requests = list()
        self._connections = list()
        self._r_list = list()
        self._w_list = list()
        self._x_list = list()

    # Методы __enter__ и __exit__ для работы с контекстным менеджером 'with'
    def __enter__(self):
        if not self._socket:
            self._socket = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Server shutdown'
        if exc_type:
            if not exc_type is KeyboardInterrupt:
                message = 'Server stopped with error'
        logging.info(message, exc_info=exc_val)
        return True

    def run(self):
        self.init_session()
        while True:
            self._accept_client()
            self._handle_clients()
            self._read()
            self._write()

    def init_session(self):
        self._socket.bind((self.host, self.port, ))
        # docks.python.org: Empty sequences are allowed, but acceptance of three empty sequences is platform-dependent.
        # (It is known to work on Unix but not on Windows.)
        # Для винды устанавливаем таймаут, чтобы завелся select(). С пустым списком self._connections будет
        # OSError: [WinError 10022] An invalid argument was supplied. При этом надо успеть за этот таймаут подключиться
        # клиентом к серверу. Этот костыль онли для отладки на винде
        # self._socket.settimeout(2)
        # В боевом режиме устанавливаем таймаут в 0
        self._socket.settimeout(0)
        self._socket.listen(self.clients_qty)
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
            response = self._handle_request()
            for client in self._w_list:
                Thread(target=self._write_by_single_thread, args=(client, response)).start()

    def _write_by_single_thread(self, client, response):
        try:
            client.send(response)
        except Exception:
            self._remove_client(client)

    def _handle_request(self):
        return self.handler(self._get_last_request())

    def _get_last_request(self):
        return self._requests.pop()
