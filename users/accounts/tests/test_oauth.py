from django.test import TestCase
from authlib.integrations.django_client import OAuth

from users.accounts.oauth import OAuthRequestToken


class OAuthRequestTokenTest(TestCase):
    def setUp(self):
        self.obj = OAuthRequestToken()

    def test_has_attribute_oauth_usp(self):
        self.assertTrue(hasattr(self.obj, 'oauth_usp'))

    def test_oauth_usp_instance(self):
        self.assertIsInstance(self.obj.oauth_usp, OAuth)