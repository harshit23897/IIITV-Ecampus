from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

from .views import course_list_of_faculty

urlpatterns = [
    url(r'^list/$', course_list_of_faculty, name='course_list_of_faculty'),
]