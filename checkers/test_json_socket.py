from time import sleep
from json_socket import *
import unittest
import logging

class JsonSocketTest(unittest.TestCase):

    def test_encode_message(self):
        json_socket = JsonSocket()
        data = ['test', [1, 2, 3]]

        message = json_socket.encode_message(data)

        self.assertEqual('0019["test", [1, 2, 3]]', message)


class JsonSocketServerTest(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    def test_server_call(self):
        server = JsonSocketServer()
        server.serve()
        client = JsonSocketClient()
        client.connect()

        server.on('test', lambda n, _: ['test_response', [n + 1]])
        def test_response(n, c):
            self.assertEqual(2, n)
            client.call(SOCKET_CLOSE_HANDLE, [0])

        client.on('test_response', test_response)

        response = client.call('test', [1])

        server.join()
        client.join()

    def test_multiple_connections(self):
        server = JsonSocketServer(max_clients=2)
        server.serve()
        client1 = JsonSocketClient()
        client1.connect()
        client2 = JsonSocketClient()
        client2.connect()


        client1.call(SOCKET_CLOSE_HANDLE, [0])
        client2.call(SOCKET_CLOSE_HANDLE, [0])

        client2.join()
        client1.join()
        server.join()
