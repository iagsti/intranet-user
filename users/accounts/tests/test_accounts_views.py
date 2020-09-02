from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.http import HttpRequest, QueryDict
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import AnonymousUser

from ..views import OAuthAuthorize, OAuthLogin
from ..models import UserModel
from .mock import mock_oauth
from .faker import data as user_data


class LoginViewsTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('accounts:login'))

    def test_status_code(self):
        """Status code should be 302"""
        self.assertEqual(302, self.resp.status_code)


class LoginViewsUserLogedInTest(TestCase):
    def setUp(self):
        user_data['bind'] = '[{"codigoUnidade": "14"}]'
        self.user = UserModel.objects.create_user(**user_data)
        self.client.force_login(self.user)
        self.resp = self.client.get(r('accounts:login'))

    def test_redirect_to_user_detail(self):
        """Loged in user should be redirect to user detail"""
        expected = '/auth/user'
        self.assertEqual(self.resp.url, expected)


class AuthorizeViewTest(TestCase):
    @mock_oauth
    def setUp(self):
        self.request = HttpRequest()
        query = QueryDict(
            'oauth_token=12345oauth & oauth_verifier=12345veriifer')

        self.request.GET = query

        session = SessionStore()
        setattr(self.request, 'session', session)

        request_token = dict(
            oauth_token='token123', oauth_token_secret='oauth_token_secret123',
            oauth_verifier='verifier123')
        self.request.session['_usp_authlib_request_token_'] = request_token

        setattr(self.request, 'user', AnonymousUser())

        self.obj = OAuthAuthorize()

    @ mock_oauth
    def test_user_has_been_presisted(self):
        self.obj.setup(self.request)
        self.obj.get(self.request)
        self.assertTrue(UserModel.objects.exists())

    @ mock_oauth
    def test_user_loged_in(self):
        self.obj.setup(self.request)
        self.obj.get(self.request)
        self.assertTrue(self.request.user.is_authenticated)


class OAuthLoginTest(TestCase):
    def setUp(self):
        self.obj = OAuthLogin()

    def test_next_url(self):
        request = HttpRequest()
        session = SessionStore()

        setattr(request, 'session', session)
        setattr(request, 'user', AnonymousUser())

        self.obj.setup(request)
        self.obj.get(request)

        expected = '/'
        self.assertEqual(self.obj.request.session.get('next'), expected)
