import socket
import threading 
import os

class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientSock):
        threading.Thread.__init__(self)
        self.csocket = clientSock
        print('Hello!', clientAddress)
    
    def run(self):
        working_dir = os.getcwd()
        while True:
            request = self.csocket.recv(1024).decode().split('\n')
            print(request)

            method, url, protocol = request[0].split(' ')
            url = os.path.join(working_dir, url[1:])
            print(url)

            code_error = "404 Not Found"
            body = ""

            if os.path.isdir(url):
                url = os.path.join(url,"index.htm")

            if os.path.isfile(url):
                code_error = "200 OK"
                body = open(url, 'r').read()
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + "\n\n" + body
                self.csocket.send(responce.encode())
                
            self.csocket.close()
            print("Connection close, bye!\n")

    

def main():
    server = socket.socket()
    server.bind(('127.0.0.1', 4646))
    server.listen(1)
    while True:
        clientSock, clientAddress = server.accept()
        newThread = ClientThread(clientAddress, clientSock)
        newThread.start()


if __name__ == '__main__':
    main()
