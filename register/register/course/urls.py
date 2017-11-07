from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

app_name = 'course'
from .views import course_list_of_faculty, course_detail_view, course_material_upload, files_list

urlpatterns = [
    url(r'^list/$', course_list_of_faculty, name='course_list_of_faculty'),
    url(r'^list/(?P<pk>.+)/$', course_detail_view, name='course_detail_view'),
    url(r'^(?P<pk>.+)/upload/$', course_material_upload, name='course_material_upload'),
    url(r'^(?P<pk>.+)/files_list/$', files_list, name='course_material_view'),
]