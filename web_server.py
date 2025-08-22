from configuration import working_directory, host, port, date_logs_delete, PROXY_TARGET_HOST, PROXY_TARGET_PORT
import asyncio
import time
import ssl
import os


async def write_in_file(logs, date_delete):
    if date_delete == time.localtime(time.time()):
        with open("access.log", 'r') as f:
            pass
    else:
        with open("/Users/denisbrevnov/Documents/Files/code/Python/Python_FIIT/Python_TASK/web_server_repo/web-server-university_project-/access.log", 'a', encoding="utf-8") as f:
            f.write(str(logs) + "\n")
            f.close()

async def read_requests(target_reader):
    delimiter = b'\r\n\r\n'
    requests = bytearray()
    while True:
        chunk = await target_reader.read(4096)
        if not chunk:
            break

        requests += chunk
        if delimiter in chunk:
            return requests

    return None

async def serve_client(reader, writer):
    try:
        request_bytes = await read_requests(reader)
        if request_bytes is None:
            print(f'Client unexpectedly disconnected')
            writer.close()
            await writer.wait_closed()
            return

        target_reader, target_writer = await asyncio.open_connection(PROXY_TARGET_HOST, PROXY_TARGET_PORT)
        print(f"Connected to {PROXY_TARGET_HOST}:{PROXY_TARGET_PORT}")

        target_writer.write(request_bytes)
        await target_writer.drain()

        target_response = await read_requests(target_reader)

        target_request = target_response.decode("utf-8")

        response = target_request

        writer.write(response.encode("utf-8"))
        await writer.drain()
        print('Close connection')
        writer.close()
        target_writer.close()
        await writer.wait_closed()
        await target_writer.wait_closed()
    except Exception as exception:
        print(f"Error {exception}")


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
