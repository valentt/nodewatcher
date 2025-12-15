from django.urls import re_path, include

from nodewatcher.core.frontend import components


class OAuthComponent(components.FrontendComponent):
    @classmethod
    def get_urls(cls):
        return super(OAuthComponent, cls).get_urls() + [
            re_path(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
        ]

components.pool.register(OAuthComponent)
