from web_server import get_content_from_file
import unittest
import requests
import urllib3


async def get_content_for_test(path):
    with open(path, "r") as f:
        return f.read()


def send_msg():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(
        "https://127.0.0.1:4747//Users/denisbrevnov/Documents/Files/code/Python/Python_FIIT/Python_TASK/web_server_repo/web-server-university_project-/folderserver/folderserver.htm",
        verify=False,
    )
    return response


class Tests(unittest.TestCase):

    def test_byte_package(self):
        pass

    def test_write_into_access_log(self):
        send_msg()
        with open("access.log", "r") as f:
            lines = f.readlines()
        self.assertEqual(
            lines[-1].split("|")[3], "('200 OK', 'User-Agent: python-requests/2.32.4')"
        )

    async def test_read_content_from_file(self):
        path = "/Users/denisbrevnov/Documents/Files/code/Python/Python_FIIT/Python_TASK/web_server_repo/web-server-university_project-/index.htm"
        self.assertEqual(get_content_from_file(path), get_content_for_test(path))

    def test_url_get_request(self):
        with open("folderserver/folderserver.htm", "r") as f:
            file = f.read()

        self.assertEqual(send_msg().text, file)


if __name__ == "__main__":
    unittest.main()
