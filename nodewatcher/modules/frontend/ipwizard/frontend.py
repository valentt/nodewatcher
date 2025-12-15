from django.conf import urls
from django.core import urlresolvers

from nodewatcher.core.frontend import components

from . import views


class IpWizardComponent(components.FrontendComponent):
    @classmethod
    def get_urls(cls):
        return super(IpWizardComponent, cls).get_urls() + [
            # Main wizard
            urls.url(r'^ip/wizard/$', views.WizardView.as_view(), name='wizard'),
            urls.url(r'^ip/pools/$', views.PoolListView.as_view(), name='pool_list'),

            # API endpoints
            urls.url(r'^api/ip/projects/$', views.ProjectsAPIView.as_view(), name='api_projects'),
            urls.url(r'^api/ip/countries/$', views.CountriesAPIView.as_view(), name='api_countries'),
            urls.url(r'^api/ip/regions/(?P<country_id>\d+)/$', views.RegionsAPIView.as_view(), name='api_regions'),
            urls.url(r'^api/ip/validate/$', views.ValidatePoolView.as_view(), name='api_validate'),
            urls.url(r'^api/ip/assign/$', views.AssignPoolView.as_view(), name='api_assign'),
            urls.url(r'^api/ip/project/(?P<project_id>\d+)/pools/$', views.ProjectPoolsView.as_view(), name='api_project_pools'),
            urls.url(r'^api/ip/pool-settings/(?P<pool_settings_id>\d+)/remove/$', views.RemovePoolView.as_view(), name='api_remove_pool'),
        ]


components.pool.register(IpWizardComponent)


# Add to main menu
components.menus.get_menu('main_menu').add(components.MenuEntry(
    label=components.ugettext_lazy("IP Pool Wizard"),
    url=urlresolvers.reverse_lazy('IpWizardComponent:wizard'),
    visible=lambda menu_entry, request, context: request.user.is_authenticated,
))

# Add to accounts menu
components.menus.get_menu('accounts_menu').add(components.MenuEntry(
    label=components.ugettext_lazy("IP Pool Wizard"),
    url=urlresolvers.reverse_lazy('IpWizardComponent:wizard'),
    visible=lambda menu_entry, request, context: request.user.is_authenticated,
))

components.menus.get_menu('accounts_menu').add(components.MenuEntry(
    label=components.ugettext_lazy("Project Pools"),
    url=urlresolvers.reverse_lazy('IpWizardComponent:pool_list'),
    visible=lambda menu_entry, request, context: request.user.is_authenticated,
))
