import socket
from configuration import working_directory, host, port, home_file
import threading 
import os

class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientSock):
        threading.Thread.__init__(self)
        self.csocket = clientSock
        print('Hello!', clientAddress)
    
    def run(self):
        request = []
        working_dir = working_directory
        request += self.csocket.recv(4096).decode().split('\n')

        while request[-2] != "\r":
            request += self.csocket.recv(4096).decode().split('\n')
            print(request)

        while True:
            print(len(request))
            print(request)
    
            method, url, protocol = request[0].split(' ')
            url = os.path.join(working_dir, url[1:])
            
            if os.path.isdir(url):
                url = os.path.join(url, home_file)
                
                body = open(url, 'r').read()
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()

            if url.split('/')[-1] == 'indexof':
                code_error = "200 OK"
                body = "Index of /\n"
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()

            if url.split('/')[-1] == "visited.htm":
                code_error = "200 OK"
                body = open(url, 'r').read()
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()

            if url.split('/')[-1] == "index.htm":
                code_error = "200 OK"
                body = open(url, 'r').read()
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()
            else:
                code_error = "404 Not Found"
                body = f"<html> \
                        <head></head>\
                        <body>\
                            <center>\
                                <h1>404 Not Found</h1>\
                            </center>\
                            <hr>\
                            <center>Denis server/ 1.0.0</center>\
                        </body>\
                    </html>"
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()
            
            print("Connection close, bye!\n")
    
    

def main():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    while True:
        clientSock, clientAddress = server.accept()
        newThread = ClientThread(clientAddress, clientSock)
        newThread.start()


if __name__ == '__main__':
    main()
