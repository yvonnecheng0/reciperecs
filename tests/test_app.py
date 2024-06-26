import unittest
from app import app

class RecipeRecommendationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_submit(self):
        result = self.app.post('/submit', data={'ingredients[]': 'tomato,cheese'})
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
