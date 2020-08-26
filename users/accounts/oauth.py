from django.conf import settings


class OAuthRequestToken:
    def __init__(self):
        self.oauth_usp = getattr(settings, 'OAUTH_USP')