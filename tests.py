import socket_server
import unittest

class TestClientThread(unittest.case):
    
    def setUp(self):
        self.clientthread = socket_server.ClientThread()

    def test_one(self):
        pass
