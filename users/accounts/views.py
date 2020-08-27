from django.shortcuts import render
from django.views.generic import RedirectView, View
from django.conf import settings
from django.http import HttpResponse

from .oauth import OAuthUsp


class OAuthLogin(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.redirect_uri.url

    def setup(self, request, *args, **kwargs):
        oauth_usp = OAuthUsp()
        self.redirect_uri = oauth_usp.get_authorize_redirect(request)
        return super().setup(request, *args, **kwargs)


accounts_login = OAuthLogin.as_view()


class OAuthAuthorize(View):
    def setup(self, request, *args, **kwargs):
        self.oauth_usp = OAuthUsp()
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        profile = self.oauth_usp.get_resource(request)


accounts_authorize = OAuthAuthorize.as_view()
