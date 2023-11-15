import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from app.models import User


class AuthTestsCase(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app('testing')
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def test_register(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'}
        response = self.client.post('/register', json=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('Utilisateur enregistré avec succès', response.json['message'])

    def test_register_missing_data(self):
        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post('/register', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Données de formulaire incorrectes', response.json['message'])

    @patch('app.controllers.auth.create_access_token', return_value='test_access_token')
    def test_login(self, mock_create_access_token):
        user_data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'}
        User.find_one = MagicMock(return_value=user_data)

        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/login', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['access_token'], 'test_access_token')
        mock_create_access_token.assert_called_once_with(identity='testuser')

    def test_login_invalid_user(self):
        User.find_one = MagicMock(return_value=None)

        data = {'username': 'nonexistentuser', 'password': 'testpassword'}
        response = self.client.post('/login', json=data)

        self.assertEqual(response.status_code, 401)
        self.assertIn('Nom d\'utilisateur ou mot de passe incorrect', response.json['message'])

    def test_login_missing_data(self):
        response = self.client.post('/login', json={})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Données de formulaire incorrectes', response.json['message'])


if __name__ == '__main__':
    unittest.main()
