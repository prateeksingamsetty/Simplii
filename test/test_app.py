import unittest
from src.app import app
import requests


app.testing = True

class TestModule(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_add_task(self):
        tester = app.test_client(self)
        inp = {"id": "7X9UE", "task_name": "dummy_task", "deadline": "2021-03-30 21:08", "estimate": 1, "task_type": "physical", "quant_verbal": "NA", "creat_consum": "NA", "difficulty": "3", "task_status":"Pending"}
        response = requests.post("http://127.0.0.1:5000/add_task", data=inp)
        self.assertEqual(response.status_code, 500)

    def test_delete_task(self):
        tester = app.test_client(self)
        inp = {"id": "23"}
        response = requests.post("http://127.0.0.1:5000/delete_task", data=inp)
        self.assertEqual(response.status_code, 500)

   


if __name__ == "__main__":
    unittest.main()
