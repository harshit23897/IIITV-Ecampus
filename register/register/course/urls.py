from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

from .views import course_list_of_faculty, course_detail_view

urlpatterns = [
    url(r'^list/$', course_list_of_faculty, name='course_list_of_faculty'),
    url(r'^(?P<pk>.+)/$', course_detail_view, name='course_detail_view'),
    url(r'^(?P<pk>.+)/', include('register.coursematerial.urls')),
]