from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from account.models import Account


def get_payload(value_list: dict = None):
    payload = {
        'username': 'testusername',
        'password': '1234567890',
        'confirm_password': '1234567890',
        'email': 'test@gmail.com'

    }
    if value_list:
        for key, value in value_list.items():
            payload[key] = value
            if payload[key] is None:
                payload.pop(key)
    return payload


class RegisterTestCase(TestCase):
    # TODO: Bom config not save
    def setUp(self):
        self.client = APIClient()

    def test_email_format(self):
        payload = get_payload({'email': 'abc'})
        response = self.client.post('/api/account/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'error_email_format')

    def test_remove_email(self):
        payload = get_payload({'email': None})
        response = self.client.post('/api/account/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_428_PRECONDITION_REQUIRED)
        self.assertEqual(response.data['detail'], 'email_is_required')

    def test_username_already_exists(self):
        Account.objects.create(username='testusername')
        payload = get_payload()
        response = self.client.post('/api/account/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'username_has_been_already_use')

    def test_remove_username(self):
        payload = get_payload({'username': None})
        response = self.client.post('/api/account/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_428_PRECONDITION_REQUIRED)
        self.assertEqual(response.data['detail'], 'username_is_required')
