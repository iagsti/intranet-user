from django.urls import re_path

from .views import ApiProxy


urlpatterns = [
    re_path(r'^(?P<path>.*)$', ApiProxy.as_view()),
]
