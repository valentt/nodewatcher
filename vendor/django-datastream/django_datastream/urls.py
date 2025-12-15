from django.urls import re_path, include

from tastypie import api

from . import resources

v1_api = api.Api(api_name='v1')
v1_api.register(resources.StreamResource())

urlpatterns = [
    re_path(r'^', include(v1_api.urls)),
]
