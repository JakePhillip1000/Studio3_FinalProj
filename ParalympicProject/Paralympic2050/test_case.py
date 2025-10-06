import unittest
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.http import HttpResponseRedirect 
from Paralympic2050.models import UserData

#### py manage.py test Paralympic2050

class LoginViewTests(TestCase):
    TEST_USERNAME = "testuser123"
    TEST_PASSWORD = "securepassword"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserData.objects.create(
            username=cls.TEST_USERNAME,
            password=cls.TEST_PASSWORD 
        )
        cls.client = Client()

    def test_get_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    @patch('Paralympic2050.views.redirect') 
    def test_successful_login(self, mock_redirect):
        mock_redirect.return_value = HttpResponseRedirect('/home/')

        response = self.client.post('/login/', {
            'username': self.TEST_USERNAME, 
            'password': self.TEST_PASSWORD
        })

        self.assertEqual(self.client.session.get('logged_in_user'), self.TEST_USERNAME)
        mock_redirect.assert_called_once_with("Paralympic2050:home")
        self.assertEqual(response.status_code, 302)

    def test_login_with_non_existent_username(self):
        non_existent_username = 'imaginaryuser'
        response = self.client.post('/login/', {
            'username': non_existent_username, 
            'password': self.TEST_PASSWORD
        })

        self.assertEqual(response.status_code, 200) 
        self.assertIs(response.context['username_not_exist'], True)
        self.assertIs(response.context['not_exist'], True)
        self.assertEqual(response.context['entered_username'], non_existent_username)
        self.assertNotIn('logged_in_user', self.client.session)

    def test_login_with_wrong_password(self):
        response = self.client.post('/login/', {
            'username': self.TEST_USERNAME, 
            'password': 'incorrectpassword'
        })

        self.assertEqual(response.status_code, 200) 
        self.assertIs(response.context['wrong_password'], True)
        self.assertEqual(response.context['entered_username'], self.TEST_USERNAME)
        self.assertNotIn('logged_in_user', self.client.session)

    @patch('Paralympic2050.views.redirect')
    def test_login_with_whitespace_username(self, mock_redirect):
        whitespace_username = f"  {self.TEST_USERNAME}  "
        mock_redirect.return_value = HttpResponseRedirect('/home/')

        response = self.client.post('/login/', {
            'username': whitespace_username, 
            'password': self.TEST_PASSWORD
        })

        self.assertEqual(self.client.session.get('logged_in_user'), self.TEST_USERNAME)
        self.assertEqual(response.status_code, 302)
        mock_redirect.assert_called_once()

    def test_login_case_mismatch(self):
        case_mismatch_username = self.TEST_USERNAME.upper()
        
        response = self.client.post('/login/', {
            'username': case_mismatch_username, 
            'password': self.TEST_PASSWORD
        })
        
        self.assertEqual(response.status_code, 200) 
        self.assertIs(response.context['username_not_exist'], True)

    def test_login_with_empty_username_string(self):
        empty_username = ""
        response = self.client.post('/login/', {
            'username': empty_username, 
            'password': self.TEST_PASSWORD
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context['username_not_exist'], True)
        self.assertEqual(response.context['entered_username'], empty_username)

    def test_login_with_empty_password_string(self):
        """Test POST request with an empty string for password."""
        empty_password = ""
        response = self.client.post('/login/', {
            'username': self.TEST_USERNAME, 
            'password': empty_password
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.context['wrong_password'], True)
        self.assertNotIn('logged_in_user', self.client.session)

    def test_login_with_missing_username_field_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.client.post('/login/', {'password': self.TEST_PASSWORD})