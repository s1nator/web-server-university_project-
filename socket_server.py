import socket
import threading
import os
  

def main():
    working_dir = os.getcwd()
    server = socket.socket()
    server.bind(('127.0.0.1', 4545))
    server.listen(1)
    clientSock, clientAddress = server.accept()
    while True:
        print('Hello! I am :', clientAddress)
        request = clientSock.recv(10240).decode().split('\n')
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
            clientSock.send(responce.encode())
            clientSock.close()

        print("Connection close, bye!\n")



if __name__ == '__main__':
    main()
