from django.shortcuts import render
from django.views.generic import RedirectView
from django.conf import settings


class OAuthLogin(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.redirect_uri.url

    def setup(self, request, *args, **kwargs):
        oauth_usp = getattr(settings, 'OAUTH_USP')
        usp = oauth_usp.create_client('usp')
        redirect_uri = getattr(settings, 'REDIRECT_URI')
        self.redirect_uri = usp.authorize_redirect(request, redirect_uri)
        return super().setup(request, *args, **kwargs)


accounts_login = OAuthLogin.as_view()
