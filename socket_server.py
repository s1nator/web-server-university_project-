import socket
from configuration import working_directory, host, port, home_file, value_logs_delete
import threading 
import time
import os


def write_in_file(logs, value_delete):
    with open("access.log", 'a', encoding="utf-8") as f:
        f.write(str(logs) + "\n")
        f.close()

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

        while True:
            logs = []
    
            method, url, protocol = request[0].split(' ')
            url = os.path.join(working_dir, url[1:])
            
            if os.path.isdir(url):
                url = os.path.join(url, home_file)
    
            if 'indexof' in url.split('/'):
                code_error = "200 OK"
                logs.append([request[1],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),request[0], code_error, request[2]])
                list_files = os.listdir(working_dir)
                indexof_name = "Index of /"

                body = f"<html> \
                        <head></head>\
                        <body>\
                            <h1>{indexof_name}</h1>\
                            <hr>\
                        "
                
                for file in list_files:
                    if os.path.isfile(file):
                        body += f"<h4><a href={file}>{file}</a></h4>"
                    if os.path.isdir(file):
                        working_dir = os.path.join(working_dir, file)
                        body += f"<h4><a href={working_dir}>{file}</a></h4>"
                body += f"<hr>"

                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
                    + "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()

            elif os.path.isfile(url):
                code_error = "200 OK"
                logs.append([request[1],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),request[0], code_error, request[2]])
                body = open(url, 'r').read()
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
                    + "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()

            else:
                code_error = "404 Not Found"
                logs.append([request[1],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),request[0], code_error , request[2]])
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
                responce = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + \
                      "\n\n" + body
                self.csocket.send(responce.encode())
                self.csocket.close()
            write_in_file(logs, value_logs_delete)
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
