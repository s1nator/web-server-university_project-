from web_server import write_in_file
from configuration import host, port
import unittest
import socket
import time



class Tests(unittest.TestCase):

    def test_byte_package(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        test_request = f"GET / HTTP/1.0\r\n\r\n"
        for part_of_request in test_request:
            sock.send(bytes(part_of_request, 'utf-8'))
            time.sleep(1)
        response = sock.recv(4096)



    def test_write_into_file(self):
        pass





if __name__ == '__main__':
    unittest.main()