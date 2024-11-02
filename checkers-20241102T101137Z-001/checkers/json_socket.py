import socket
import sys
import json
from threading import Thread
import logging

BIND_ADDRESS = '127.0.0.1'
BIND_PORT = 8000
SOCKET_CONNECT_HANDLE = 'connect'
SOCKET_CLOSE_HANDLE = 'disconnect'


class JsonSocket:

    def __init__(self, sock=None, raddr=None, handles={}):
        self.sock = sock
        self.handles = {}
        self.raddr = raddr

    def on(self, event, handle):
        self.handles[event] = handle

    def call_handle(self, event, args):
        res = None
        if event in self.handles:
            logging.info('call_handle "%s"' % event)
            res = self.handles[event](*args)
        else:
           logging.info('No handle for "%s"' % event)

        return res

    def start_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def encode_message(self, data):
        json_message = json.dumps(data)

        return str(len(json_message)).zfill(4) + json_message

    def wait_data(self, sock, send_response=False, disconnected=False):
        while not disconnected:
            data = self.read_data(sock)

            if data:
                event, args = tuple(data)
                args.append(self)
                if event == SOCKET_CLOSE_HANDLE:
                    disconnected = True
                    args = [sock]

                res = self.call_handle(event, args)
                if send_response and res:
                    self.send_data(res, sock)

    def send_data(self, data, socket=None):
        if not socket:
            socket = self.sock
        logging.info('sent %s' % data)
        socket.sendall(self.encode_message(data).encode())

    def read_data(self, socket):
        while True:
            message_length_recv = socket.recv(4)
            if message_length_recv:
                message_length = int(message_length_recv)

                if message_length > 0:
                    data = ''
                    while True:
                        data = data + socket.recv(message_length).decode()
                        logging.info('received %s from %s', data, self.raddr)
                        if len(data) >= message_length:
                            break

                    return json.loads(data)

        return None


class JsonSocketClient(Thread, JsonSocket):

    def __init__(self, address=BIND_ADDRESS, port=BIND_PORT):
        Thread.__init__(self)
        JsonSocket.__init__(self)

        self.daemon = True
        self.on(SOCKET_CLOSE_HANDLE, self.close)
        self.address = address
        self.port = port

    def connect(self):
        self.start_socket()
        self.raddr = (self.address, self.port)
        self.sock.connect(self.raddr)
        self.start()

    def call(self, handle, data=None):
        self.send_data([handle, data], self.sock)

    def run(self):
        self.wait_data(self.sock, False)

    def close(self, sock):
        sock.close()
        logging.info('client closed connection')


class JsonSocketServer(Thread, JsonSocket):

    def __init__(self, bind_port=BIND_PORT, max_clients=1):
        Thread.__init__(self)
        JsonSocket.__init__(self)

        self.daemon = True
        self.connections = []
        self.max_clients = max_clients
        self.bind_port = bind_port

    def serve(self):
        self.start_socket()
        self.sock.bind((BIND_ADDRESS, self.bind_port))
        self.sock.listen(1)
        self.start()

    def run(self):
        while len(self.connections) < self.max_clients:
            logging.info('waiting for a connection')
            connection, client_address = self.sock.accept()
            connection_handler = JsonSocketServerConnection(connection, client_address, self.handles)
            self.connections.append(connection_handler)
            logging.info('connection from %s', client_address)

            connection_handler.start()
            active_connections = list(filter(lambda connection: connection.connected, self.connections))
            if len(active_connections) == 0:
                break
        self.close()

    def close(self):
        logging.info('server closed connection')
        self.sock.close()


class JsonSocketServerConnection(Thread, JsonSocket):

    def __init__(self, sock, client_address, handles):
        Thread.__init__(self)
        JsonSocket.__init__(self, sock, client_address)

        self.handles = handles
        self.connected = True
        self.sock = sock
        self.on(SOCKET_CLOSE_HANDLE, self.close)

    def run(self):
        if SOCKET_CONNECT_HANDLE in self.handles:
            self.call_handle(SOCKET_CONNECT_HANDLE, [self])
        self.wait_data(self.sock, True)
        self.sock.close()

    def close(self, _):
        self.connected = False
        logging.info('server closed client connection %s', self.raddr)

        return ['disconnect', []]