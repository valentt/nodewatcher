from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, include


# Importing nodewatcher.core.frontend.urls auto-discovers frontend components.
from nodewatcher.core.api import urls as api_urls
from nodewatcher.core.frontend import urls as frontend_urls

admin.autodiscover()

urlpatterns = [
    # Language switching.
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    # Registry.
    re_path(r'^registry/', include(('nodewatcher.core.registry.urls', 'registry'), namespace='registry')),

    # API.
    re_path(r'^api/v3/', include((api_urls.v3_api.urls, 'apiv3'), namespace='apiv3')),
    re_path(r'^api/', include((api_urls.v1_api.urls, 'api'), namespace='api')),

    # Django admin interface.
    re_path(r'^admin/', admin.site.urls),

    # Frontend.
    re_path(r'^', include(frontend_urls)),
]

handler403 = 'missing.views.forbidden_view'

if settings.DEBUG:
    from missing import views as missing_views
    from django.views import defaults

    urlpatterns += [
        re_path(r'^400/$', lambda request: defaults.bad_request(request, Exception("Dummy exception."))),
        # See CSRF_FAILURE_VIEW in settings.py as well.
        re_path(r'^403/$', lambda request: missing_views.forbidden_view(request, Exception("Dummy exception."))),
        re_path(r'^404/$', lambda request: defaults.page_not_found(request, Exception("Dummy exception."))),
        re_path(r'^500/$', defaults.server_error),
    ]

if settings.DEBUG:
    # Serve static files in DEBUG mode.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
