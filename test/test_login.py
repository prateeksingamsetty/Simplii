import unittest
from src.app import app
import requests


app.testing = True

class TestModule(unittest.TestCase):
        
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get("/login", content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
        
if __name__ == "__main__":
    unittest.main()
        
    
