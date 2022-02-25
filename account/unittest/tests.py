import datetime
import random
import string
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from account.models import Account, Clocking


def create_super_user(username=None, email=None, password=None):
    if username is None:
        username = ''.join(random.sample(string.ascii_lowercase, 6))
    if email is None:
        email = '%s@domain.com' % username
    if password is None:
        password = '1234'
    account = Account.objects.create_superuser(username, password)
    account.email = email
    account.save(update_fields=['email'])
    return account


class ClockingAPITestCase(TestCase):
    def setUp(self):
        self.account = create_super_user()
        self.client = APIClient()
        self.client.force_authenticate(self.account)
        self.base_url = '/api/account/'

    def test_checkIn(self):
        response = self.client.get('/api/account/clock/clockIn/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_checkOut(self):
        user = create_super_user()
        client = APIClient()
        client.force_authenticate(user)
        clocking = Clocking.objects.create(account_id=user.id, clock_in=(datetime.datetime.now() - timedelta(hours=5)))
        response = client.get('/api/account/clock/clockOut/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
