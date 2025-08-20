from configuration import working_directory, host, port, home_file, date_logs_delete
import asyncio
import time
import os


async def write_in_file(logs, date_delete):
    if date_delete == time.localtime(time.time()):
        with open("access.log", 'r') as f:
            pass
    else:
        with open("access.log", 'a', encoding="utf-8") as f:
            f.write(str(logs) + "\n")
            f.close()

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
    working_dir = working_directory

    logs = []

    request_lines = request.splitlines()[0]

    method, url, protocol = request_lines.split(" ", 2)
    url = os.path.join(working_dir, url[1:])

    if os.path.isdir(url):
        url = os.path.join(url, home_file)

    if 'indexof' in url.split('/'):
        code_error = "200 OK"
        request_for_logs = request.split("\n")

        logs.append([request_for_logs[1].strip("\r"),
                      time.strftime( "%Y-%m-%d %H:%M:%S", time.localtime()),
                     request_for_logs[0].strip("\r"),
                     code_error,
                     request_for_logs[2].strip("\r"),
                     request_for_logs[3].strip("\r")])

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

        response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
            + "\n\n" + body

    elif os.path.isfile(url):
        code_error = "200 OK"
        request_for_logs = request.split("\n")
        logs.append(
            [request_for_logs[1].strip("\r"),
             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
             request_for_logs[0].strip("\r"),
             code_error,
             request_for_logs[2].strip("\r"),
             request_for_logs[3].strip("\r")])

        body = open(url, 'r').read()
        response = f"HTTP/1.1 {code_error}\n" + "Server:my_server" \
            + "\n\n" + body


    else:
        code_error = "404 Not Found"
        request_for_logs = request.split("\n")
        logs.append(
            [request_for_logs[1].strip("\r"),
             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
             request_for_logs[0].strip("\r"),
             code_error,
             request_for_logs[2].strip("\r"),
             request_for_logs[3].strip("\r")])

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
    server = await asyncio.start_server(serve_client, host=host, port=port)

    address = server.sockets[0].getsockname()
    print("Serving on ", address)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down")
