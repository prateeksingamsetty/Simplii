import unittest
from src.app import app
import requests


app.testing = True

class TestModule(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_signup(self):
        tester = app.test_client(self)
        response = tester.get("/signup", content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_add_task(self):
        tester = app.test_client(self)
        inp = {"taskName": "dummy_task", "deadline": "2021-03-30T21:08", "estimateInput": 1, "taskType": "physical",
               'quant/verbal': "NA", "contentconsump": "NA", "difficulty": "3"}
        response = requests.post("http://127.0.0.1:5000/add_task", data=inp)
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        tester = app.test_client(self)
        inp = {"id": "23"}
        response = requests.post("http://127.0.0.1:5000/delete_task", data=inp)
        self.assertEqual(response.status_code, 200)

    def test_update_user_info(self):
        tester = app.test_client(self)
        inp = {"name": "user1", "email": "user1@gmail.com", "emailChoose": "user1@gmail.com"}
        response = requests.post("http://127.0.0.1:5000/update_user_info", data=inp)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
