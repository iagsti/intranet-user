import json
from django.test import TestCase
from django.conf import settings

from ..views import ApiProxy
from ..models import Upstreams
from .mock import mock_uri, user
from users.accounts.models import UserModel


class ApiProxyTest(TestCase):
    def setUp(self):
        self.obj = ApiProxy()

    def test_instance(self):
        self.assertIsInstance(self.obj, ApiProxy)

    def test_default_upstream(self):
        expected = getattr(settings, 'DEFAULT_UPSTREAM')
        self.assertEqual(expected, self.obj.upstream)


class ApiProxyTestGetLogedIn(TestCase):
    @mock_uri
    def setUp(self):
        self.make_upstream()
        user = self.mock_user()
        self.client.force_login(user)
        self.resp = self.client.get('/api/test')

    def test_status_code(self):
        self.assertEqual(200, self.resp.status_code)

    def test_response_body(self):
        expected = {'content': 'content'}
        resp = json.loads(self.resp.content)
        self.assertDictEqual(expected, resp)

    def make_upstream(self):
        upstream = {'path': '/api/test/', 'upstream': 'http://example.com'}
        Upstreams.objects.create(**upstream)

    def mock_user(self):
        return UserModel.objects.create_user(**user)


class ApiProxyTestGetLoggedOut(TestCase):
    @mock_uri
    def setUp(self):
        self.make_upstream()
        self.resp = self.client.get('/api/test')

    def test_status_code(self):
        self.assertEqual(302, self.resp.status_code)

    def test_redirected_url(self):
        expected = getattr(settings, 'LOGIN_UPSTREAM')
        self.assertEqual(expected, self.resp.url)

    def make_upstream(self):
        upstream = {'path': '/api/test/', 'upstream': 'http://example.com'}
        Upstreams.objects.create(**upstream)
