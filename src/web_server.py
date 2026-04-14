import asyncio
import aiofiles
import multiprocessing
import time
import ssl
import os
from async_lru import alru_cache
from configuration import config

@alru_cache(maxsize=128)
async def get_content_from_file(url):
    try:
        async with aiofiles.open(url, "r", encoding="utf-8") as f:
            return await f.read()
    except Exception:
        return ""

class Logger:
    @staticmethod
    @alru_cache(maxsize=128)
    async def write_to_file(logs, date_delete):
        current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_path = os.path.join(config.working_directory or "", "access.log")
        if date_delete == current_time_str:
            async with aiofiles.open(log_path, "w", encoding="utf-8") as f:
                pass
        else:
            async with aiofiles.open(log_path, "a", encoding="utf-8") as f:
                await f.write(str(logs) + "\n")

    @classmethod
    async def log_request(cls, code_error, request):
        logs = ""
        request_lines = request.split("\n")
        get_for_logs = request_lines[0].strip("\r")
        host_for_logs = "Unknown"
        user_agent_for_logs = "Unknown"
        accept_for_logs = "*/*"

        for line in request_lines:
            parts = line.split()
            if not parts: continue
            if "Host:" == parts[0]: host_for_logs = line.strip("\r")
            if "User-Agent:" == parts[0]: user_agent_for_logs = line.strip("\r")
            if "Accept:" == parts[0]: accept_for_logs = line.strip("\r")
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logs = f"{host_for_logs}|{current_time}|{get_for_logs}|{code_error, user_agent_for_logs}|{accept_for_logs}"
        return logs

class RequestHandler:
    async def handle(self, reader, writer):
        request_bytes = await self._read_requests(reader)
        if not request_bytes:
            writer.close()
            await writer.wait_closed()
            return
            
        request = request_bytes.decode("utf-8")

        if config.proxy_pass_host:
            await self._handle_proxy(request, writer)
        else:
            response = await self._handle_local(request)
            writer.write(response.encode("utf-8"))
            await writer.drain()
            writer.close()
            await writer.wait_closed()

    async def _read_requests(self, reader):
        delimiter = b"\r\n\r\n"
        requests = bytearray()
        while True:
            chunk = await reader.read(4096)
            if not chunk: break
            requests += chunk
            if delimiter in chunk: return requests
        return None

    async def _handle_proxy(self, request, writer):
        target_reader, target_writer = await asyncio.open_connection(
            config.proxy_pass_host, config.proxy_pass_port
        )
        target_writer.write(request.encode("utf-8"))
        await target_writer.drain()
        
        try:
            response_target = await asyncio.wait_for(self._read_requests(target_reader), timeout=5)
            if response_target:
                writer.write(response_target)
                await writer.drain()
        except asyncio.TimeoutError:
            pass
        finally:
            target_writer.close()
            await target_writer.wait_closed()
            writer.close()
            await writer.wait_closed()

    async def _handle_local(self, request):
        request_lines = request.splitlines()[0]
        method, url, protocol = request_lines.split(" ", 2)
        
        virtual_host = "127.0.0.1"
        for line in request.split("\n"):
            if "Host:" in line.split():
                virtual_host = line.split()[1]
                
        normalized_url = os.path.normpath(url.lstrip("/"))
        if normalized_url.startswith(".."):
            return await self._create_response(request, "403 Forbidden", "<h1>403 Forbidden</h1>")
            
        path = os.path.normpath(os.path.join(config.working_directory, normalized_url))
        
        if not path.startswith(os.path.normpath(config.working_directory)):
             return await self._create_response(request, "403 Forbidden", "<h1>403 Forbidden</h1>")
             
        path_to_start_file = os.path.join(config.working_directory, "index.htm")
        
        if virtual_host == "site_nginx.com":
            path = os.path.join(config.working_directory, "site_nginx_com")
            path_to_start_file = os.path.join(path, "index.htm")
        elif virtual_host == "site_aiohttp.com":
            path = os.path.join(config.working_directory, "site_aiohttp_com")
            path_to_start_file = os.path.join(path, "index.htm")

        full_path_parts = path.split(os.sep)
        if "web-server-university_project-" not in full_path_parts and "Users" in full_path_parts or "etc" in full_path_parts:
            return await self._create_response(request, "404 Not Found", "<h1>404 Not Found</h1>")

        if url == "/":
            body = await get_content_from_file(path_to_start_file)
            return await self._create_response(request, "200 OK", body)
            
        if url.endswith("indexof") or url.endswith("indexof/"):
             return await self._handle_directory(request, config.working_directory, url, is_index_of=True)
            
        if os.path.isdir(path):
            return await self._handle_directory(request, path, url)
            
        file_path = path if os.path.isfile(path) else os.path.join(config.working_directory, url.split("/")[-1])
        if os.path.isfile(file_path):
            body = await get_content_from_file(file_path)
            return await self._create_response(request, "200 OK", body)

        return await self._create_response(request, "404 Not Found", "<h1>404 Not Found</h1>")

    async def _handle_directory(self, request, path, url, is_index_of=False):
        list_files = os.listdir(path)
        title = "Index of /" if is_index_of else url.split("/")[-1]
        body = f"<html><head></head><body><h1>{title}</h1><hr>"
        
        base_url = "/" if is_index_of or url == "/indexof" or url == "/indexof/" else url.rstrip("/") + "/"
        
        if not is_index_of and url not in ("/", "/indexof", "/indexof/"):
             parent_url = os.path.dirname(url.rstrip("/"))
             parent_url = "/indexof" if parent_url == "/" else parent_url
             if not parent_url.endswith("/") and parent_url != "/indexof":
                 parent_url += "/"
             body += f"<h4><a href='{parent_url}'>../ (Parent Directory)</a></h4>"
        
        for file in list_files:
            file_url = f"{base_url}{file}" if base_url != "/" else f"/{file}"
            
            if os.path.isdir(os.path.join(path, file)):
                 file_url += "/"
                 
            body += f"<h4><a href='{file_url}'>{file}</a></h4>"
            
        body += "<hr></body></html>"
        
        return await self._create_response(request, "200 OK", body)

    async def _create_response(self, request, code, body):
        logs = await Logger.log_request(code, request)
        await Logger.write_to_file(logs, config.date_logs_delete)
        return f"HTTP/1.1 {code}\nContent-Type: text/html; charset=utf-8\n\n{body}"


class WebServer:
    def __init__(self, host, port, workers, cert_file="cert.pem", key_file="key.pem"):
        self.host = host
        self.port = port
        self.workers = workers
        self.cert_file = cert_file
        self.key_file = key_file

    async def serve_client(self, reader, writer):
        handler = RequestHandler()
        await handler.handle(reader, writer)

    async def run(self):
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        if os.path.exists(self.cert_file) and os.path.exists(self.key_file):
            ctx.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
        
        server = await asyncio.start_server(
            self.serve_client, host=self.host, port=self.port, ssl=ctx if os.path.exists(self.cert_file) else None, reuse_port=True
        )
        print(f"Serving on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()

    def start(self):
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            print("\nShutting down")

    def run_multiprocess(self):
        processes = []
        for _ in range(self.workers):
            p = multiprocessing.Process(target=self.start)
            processes.append(p)
            p.start()
        for p in processes:
            p.join()


if __name__ == "__main__":
    server = WebServer(config.host, config.port, config.quantity_workers)
    server.run_multiprocess()
