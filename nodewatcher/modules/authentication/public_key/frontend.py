from django.urls import re_path
from django import urls as urlresolvers

from nodewatcher.core.api import urls as api_urls
from nodewatcher.core.frontend import components

from . import views


class PublicKeyComponent(components.FrontendComponent):
    @classmethod
    def get_urls(cls):
        return super(PublicKeyComponent, cls).get_urls() + [
            re_path(r'^my/public_keys/$', views.ListPublicKeys.as_view(), name='list'),
            re_path(r'^my/public_keys/add/$', views.AddPublicKey.as_view(), name='add'),
            re_path(r'^my/public_keys/(?P<pk>[^/]+)/remove/$', views.RemovePublicKey.as_view(), name='remove'),
        ]

components.pool.register(PublicKeyComponent)


api_urls.v3_api.register('user_authentication_key', views.UserAuthenticationKeyViewSet)


components.menus.register(components.Menu('public_key_menu'))


components.menus.get_menu('accounts_menu').add(components.MenuEntry(
    label=components.ugettext_lazy("My Public Keys"),
    url=urlresolvers.reverse_lazy('PublicKeyComponent:list'),
    visible=lambda menu_entry, request, context: request.user.is_authenticated,
))

components.menus.get_menu('public_key_menu').add(components.MenuEntry(
    label=components.ugettext_lazy("Add Public Key"),
    url=lambda menu_entry, context: urlresolvers.reverse('PublicKeyComponent:add'),
))
