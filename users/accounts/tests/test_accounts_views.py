from django.test import TestCase
from django.shortcuts import resolve_url as r


class LoginViewsTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('accounts:login'))

    def test_status_code(self):
        """Status code should be 302"""
        self.assertEqual(302, self.resp.status_code)
