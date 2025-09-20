from web_server import get_content_from_file
from configuration import host, port
import time
import unittest
import requests
import urllib3


def get_content_for_test(path):
    with open(path, "r") as f:
        return f.read()


def send_msg_for_test_write_logs():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {"Host": "127.0.0.1:4747"}
    response = requests.get(
        "https://127.0.0.1:4747//Users/denisbrevnov/Documents/Files/code/Python/Python_FIIT/Python_TASK/web_server_repo/web-server-university_project-/folderserver/folderserver.htm",
        headers=headers,
        verify=False,
    )
    return response


def send_msg_for_read_up_working_directory():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {"Host": "127.0.0.1:4747"}
    response = requests.get(
        "https://127.0.0.1:4747/../../../../../../etc/passwd",
        headers=headers,
        verify=False,
    )
    return response


def send_msg_for_host_test():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {"Host": "site_nginx.com"}
    url = "https://127.0.0.1:4747/"
    response = requests.get(url, headers=headers, verify=False)
    return response


def send_part_request():
    yield "/"
    time.sleep(1)
    yield "/"
    time.sleep(1)
    yield "/"
    time.sleep(1)
    yield "/"


class Tests(unittest.IsolatedAsyncioTestCase):

    def test_byte_package(self):
        url = f"https://{host}:{port}/"
        response = requests.get(
            url,
            data=send_part_request(),
            headers={"Content-Type": "text/plain"},
            verify=False,
        )
        self.assertEqual(200, response.status_code)

    def test_virtual_host(self):
        send_msg_for_host_test()
        with open("access.log", "r") as f:
            lines = f.readlines()
        self.assertEqual(lines[-1].split("|")[0], "Host: site_nginx.com")

    def test_write_into_access_log(self):
        send_msg_for_test_write_logs()
        with open("access.log", "r") as f:
            lines = f.readlines()
        self.assertEqual(
            lines[-1].split("|")[3], "('200 OK', 'User-Agent: python-requests/2.32.4')"
        )

    def test_read_up_directory(self):
        send_msg_for_read_up_working_directory()
        with open("access.log", "r") as f:
            lines = f.readlines()
        self.assertEqual(
            lines[-1].split("|")[3],
            "('404 Not Found', 'User-Agent: python-requests/2.32.4')",
        )

    async def test_read_content_from_file(self):
        path = "/Users/denisbrevnov/Documents/Files/code/Python/Python_FIIT/Python_TASK/web_server_repo/web-server-university_project-/index.htm"
        file_content = await get_content_from_file(path)
        self.assertEqual(file_content, get_content_for_test(path))

    def test_url_get_request(self):
        with open("folderserver/folderserver.htm", "r") as f:
            file = f.read()

        self.assertEqual(send_msg_for_test_write_logs().text, file)


if __name__ == "__main__":
    unittest.main()
