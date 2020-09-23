from django.test import TestCase
from django.db import models
from django.db.models.fields import CharField, URLField

from ..models import Upstreams


class UpstreamsTest(TestCase):
    def setUp(self):
        self.obj = Upstreams()

    def test_upstream_instance(self):
        self.assertIsInstance(self.obj, models.Model)

    def test_has_attributes(self):
        """Upstream model should have attributes"""
        attributes = ('path', 'upstream')

        for expected in attributes:
            with self.subTest():
                self.assertTrue(hasattr(self.obj, expected))

    def test_attributes_instances(self):
        self.assertIsInstance(Upstreams.path.field, CharField)
        self.assertIsInstance(Upstreams.upstream.field, URLField)

    def test_create_upstream(self):
        upstream = {'path': '/test', 'upstream': 'http://upstream.com'}
        Upstreams.objects.create(**upstream)
        self.assertTrue(Upstreams.objects.exists())
