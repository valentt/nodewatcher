from django.urls import re_path
from django import urls as urlresolvers

from nodewatcher.core.frontend import components

from . import views


class IpWizardComponent(components.FrontendComponent):
    @classmethod
    def get_urls(cls):
        return super(IpWizardComponent, cls).get_urls() + [
            # Main wizard
            re_path(r'^ip/wizard/$', views.WizardView.as_view(), name='wizard'),
            re_path(r'^ip/pools/$', views.PoolListView.as_view(), name='pool_list'),

            # API endpoints
            re_path(r'^api/ip/projects/$', views.ProjectsAPIView.as_view(), name='api_projects'),
            re_path(r'^api/ip/countries/$', views.CountriesAPIView.as_view(), name='api_countries'),
            re_path(r'^api/ip/regions/(?P<country_id>\d+)/$', views.RegionsAPIView.as_view(), name='api_regions'),
            re_path(r'^api/ip/validate/$', views.ValidatePoolView.as_view(), name='api_validate'),
            re_path(r'^api/ip/assign/$', views.AssignPoolView.as_view(), name='api_assign'),
            re_path(r'^api/ip/project/(?P<project_id>\d+)/pools/$', views.ProjectPoolsView.as_view(), name='api_project_pools'),
            re_path(r'^api/ip/pool-settings/(?P<pool_settings_id>\d+)/remove/$', views.RemovePoolView.as_view(), name='api_remove_pool'),
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
