import unittest
from src.app import app
import requests
import re

app.testing = True

class TestModule(unittest.TestCase):
    pass
    # def test_invalid_login(self):
    #     tester = app.test_client(self)
    #     inp = {"userid": "sriram123", "password": "kjdnvskcds"}
    #     response = requests.post("http://127.0.0.1:5000/login", data=inp, follow_redirects = True)
    #     self.assertTrue(re.search('Error: The entered user ID does not exist, please login with valid credentials or sign up.', response.get_data(as_text = True)))

if __name__ == "__main__":
        unittest.main()
