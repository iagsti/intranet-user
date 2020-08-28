from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.http import HttpRequest, QueryDict

from ..views import OAuthAuthorize
from ..models import UserModel
from .mock import mock_oauth


class LoginViewsTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('accounts:login'))

    def test_status_code(self):
        """Status code should be 302"""
        self.assertEqual(302, self.resp.status_code)


class AuthorizeViewTest(TestCase):
    @mock_oauth
    def setUp(self):
        self.request = HttpRequest()
        query = QueryDict(
            'oauth_token=12345oauth & oauth_verifier=12345veriifer')
        self.request.GET = query
        setattr(self.request, 'session', {'_usp_authlib_request_token_': {
                'oauth_token': 'token123', 'oauth_token_secret': 'secret123',
                'oauth_verifier': 'verifier123'}})
        self.obj = OAuthAuthorize()

    @mock_oauth
    def test_user_has_been_presisted(self):
        self.obj.setup(self.request)
        self.obj.get(self.request)
        self.assertTrue(UserModel.objects.exists())

    @mock_oauth
    def test_user_loged_in(self):
        self.obj.setup(self.request)
        self.obj.get(self.request)
        self.assertTrue(self.request.user_is_authenticated)
