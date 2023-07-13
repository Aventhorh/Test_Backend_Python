import unittest
from services.UserService import app

class MainTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_create_user(self):
        data = {
            'username': 'test_user',
            'email': 'test@example.com'
        }
        response = self.client.post('/users', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        user_id = 1
        response = self.client.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
