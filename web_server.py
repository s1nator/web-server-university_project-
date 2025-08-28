from configuration import working_directory, host, port, date_logs_delete
import asyncio
import aiofiles
import aiohttp
import time
import ssl
import os



async def write_in_file(logs, date_delete):
    current_time = time.localtime()
    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    if date_delete == current_time_str:
        async with aiofiles.open("access.log", 'r') as f:
            pass
    else:
        async with aiofiles.open(os.path.join(working_directory, "access.log"), 'a', encoding="utf-8") as f:
            await f.write(str(logs) + "\n")
            await f.close()


async def read_requests(reader):
    delimiter = b'\r\n\r\n'
    requests = bytearray()
    while True:
        chunk = await reader.read(4096)
        if not chunk:
            break

        requests += chunk
        if delimiter in chunk:
            return requests

    return None


async def serve_client(reader, writer):

    request_bytes = await read_requests(reader)
    if request_bytes is None:
        print(f'Client unexpectedly disconnected')
        writer.close()
        await writer.wait_closed()
        return

    request = request_bytes.decode("utf-8")
    response = await handle_request(request)

    writer.write(response.encode("utf-8"))
    await writer.drain()
    print('Close connection')
    writer.close()
    await writer.wait_closed()


async def handle_request(request):

    logs = ""
    full_path = []
    request_lines = request.splitlines()[0]
    method, url, protocol = request_lines.split(" ", 2)
    virtual_host = str(request.split("\n")[1].strip("\r").split("Host: ")[1])
    path_to_start_file = "index.htm"


    if virtual_host == "127.0.0.1":
        path = os.path.join(working_directory, url)

    elif virtual_host == "site_nginx.com":
        path = os.path.join(working_directory, "site_nginx_com")
        path_to_start_file = os.path.join(path, path_to_start_file)


    elif virtual_host == "site_aiohttp.com":
        path= os.path.join(working_directory, "site_aiohttp_com")
        path_to_start_file = os.path.join(path, path_to_start_file)

    else:
        path = os.path.join(working_directory, url)

    for word in path.split("/"):
        full_path.append(str(word))


    if "web-server-university_project-" not in full_path and "Users" in full_path:
        code_error = "404 Not Found"
        request_for_logs = request.split("\n")
        logs += f"{request_for_logs[1].strip("\r")}|{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}|{request_for_logs[0].strip("\r")}|{code_error, request_for_logs[2].strip("\r")}|{request_for_logs[3].strip("\r")}"
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
        response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + \
                   "\n\n" + body

        await write_in_file(logs, date_logs_delete)
        return response


    if url == "/":
        code_error = "200 OK"
        request_for_logs = request.split("\n")
        logs += f"{request_for_logs[1].strip("\r")}|{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}|{request_for_logs[0].strip("\r")}|{code_error, request_for_logs[2].strip("\r")}|{request_for_logs[3].strip("\r")}"
        with open(path_to_start_file, "r", encoding="utf-8") as f:
            body = f.read()
        response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
                   + "\n\n" + body

    elif os.path.isdir(path):

        code_error = "200 OK"
        request_for_logs = request.split("\n")
        logs += f"{request_for_logs[1].strip("\r")}|{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}|{request_for_logs[0].strip("\r")}|{code_error, request_for_logs[2].strip("\r")}|{request_for_logs[3].strip("\r")}"
        list_files = os.listdir(path)
        name_folder = url.split("/")[-1]
        body = f"<html> \
                        <head></head>\
                        <body>\
                            <h1>{name_folder}</h1>\
                            <hr>\
                        "

        for file in list_files:
            path = os.path.join(url, file)
            if os.path.isfile(path):
                body += f"<h4><a href={path}>{file}</a></h4>"
            if os.path.isdir(path):
                body += f"<h4><a href={path}>{file}</a></h4>"
        body += f"<hr>"

        response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
                   + "\n\n" + body


    elif os.path.isfile(path.split("/")[-1]) or os.path.isfile(path):

        code_error = "200 OK"
        request_for_logs = request.split("\n")
        logs += f"{request_for_logs[1].strip("\r")}|{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}|{request_for_logs[0].strip("\r")}|{code_error, request_for_logs[2].strip("\r")}|{request_for_logs[3].strip("\r")}"
        if os.path.isfile(url.split("/")[-1]) and url.split("/")[1] != 'Users':
            body = open(url.split("/")[-1], "rb").read().decode("utf-8")
            response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
                       + "\n\n" + body
        elif os.path.isfile(url):
            body = open(path, "rb").read().decode("utf-8")
            response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
                + "\n\n" + body



    elif 'indexof' == path.split('/')[-1]:

        code_error = "200 OK"
        request_for_logs = request.split("\n")

        logs += f"{request_for_logs[1].strip("\r")}|{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}|{request_for_logs[0].strip("\r")}|{code_error, request_for_logs[2].strip("\r")}|{request_for_logs[3].strip("\r")}"

        list_files = os.listdir(working_directory)
        index_of_name = "Index of /"

        body = f"<html> \
                <head></head>\
                <body>\
                    <h1>{index_of_name}</h1>\
                    <hr>\
                "

        for file in list_files:
            if os.path.isfile(file):
                body += f"<h4><a href={file}>{file}</a></h4>"
            if os.path.isdir(file):
                working_dir = os.path.join(working_directory, file)
                body += f"<h4><a href={working_dir}>{file}</a></h4>"
        body += f"<hr>"

        response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
            + "\n\n" + body

    else:
        code_error = "404 Not Found"
        request_for_logs = request.split("\n")
        logs += f"{request_for_logs[1].strip("\r")}|{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}|{request_for_logs[0].strip("\r")}|{code_error, request_for_logs[2].strip("\r")}|{request_for_logs[3].strip("\r")}"
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
        response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" + \
                   "\n\n" + body

    await write_in_file(logs, date_logs_delete)
    return response




async def main():
    sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslcontext.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    server = await asyncio.start_server(serve_client, host=host, port=port, ssl=sslcontext)
    address = server.sockets[0].getsockname()
    print("Serving on ", address)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down")
