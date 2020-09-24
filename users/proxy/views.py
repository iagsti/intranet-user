from django.conf import settings
from django.shortcuts import redirect
from revproxy.views import ProxyView

from .models import Upstreams


class ApiProxy(ProxyView):
    upstream = getattr(settings, 'DEFAULT_UPSTREAM')
    add_remote_user = True

    def get_upstream(self, path):
        self.set_upstream_for(self.request)

        return super(ApiProxy, self).get_upstream(path)

    def set_upstream_for(self, request):
        path = request.get_full_path()
        upstreams = Upstreams.objects.filter(path=path)
        if (upstreams.count() > 0):
            self.upstream = upstreams.first().upstream

    def dispatch(self, request, path):
        if not request.user.is_authenticated:
            return redirect(getattr(settings, 'LOGIN_UPSTREAM'))

        return super().dispatch(request, path)
