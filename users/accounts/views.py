from django.views.generic import RedirectView, View
from django.contrib.auth import login

from .oauth import OAuthUsp
from .transform import Transform
from .models import UserModel


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
        self.profile = self.oauth_usp.get_resource(request)
        self.data_transform()
        self.persist_user()
        self.authenticate_user(request)

    def data_transform(self):
        transform = Transform()
        self.profile = transform.transform_data(self.profile)

    def persist_user(self):
        self.user = UserModel.objects.create_user(**self.profile)

    def authenticate_user(self, request):
        login(request=request, user=self.user)


accounts_authorize = OAuthAuthorize.as_view()
