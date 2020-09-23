from django.db import models
from django.utils.translation import gettext as _


class Upstreams(models.Model):
    path = models.CharField(_("path"), max_length=50)
    upstream = models.URLField(_(""), max_length=200)
