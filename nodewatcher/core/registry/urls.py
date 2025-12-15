from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'evaluate_forms/(?P<regpoint_id>.+?)/(?:(?P<root_id>.+?)/)?$', views.evaluate_forms, name='evaluate_forms'),
]
