import unittest
import requests


BASE_URL = "http://localhost:8080/"

class TestSmoke(unittest.TestCase):
    def test_home_and_login(self):
        self.assertEqual(requests.get(BASE_URL).status_code, 200)
        self.assertEqual(requests.get(BASE_URL+'login').status_code, 200)


if __name__=='__main__':
    unittest.main()