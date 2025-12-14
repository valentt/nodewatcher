from django.conf import urls

from nodewatcher.core.frontend import components

from . import views


class LandingComponent(components.FrontendComponent):
    @classmethod
    def get_main_url(cls):
        return {
            'regex': r'^$',
            'view': views.LandingPage.as_view(),
            'name': 'landing',
        }

    @classmethod
    def get_urls(cls):
        return [
            urls.url(r'^old/$', views.OldHomepage.as_view(), name='old'),
        ]

components.pool.register(LandingComponent)
