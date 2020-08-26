from django.urls import path
from .views import accounts_login

app_name = 'accounts'

urlpatterns = [
    path('login', accounts_login, name='login')
]
