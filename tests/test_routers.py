import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_books(self):
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, 200)
