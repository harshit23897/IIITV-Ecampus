from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

from .views import course_material_upload, files_list, download

urlpatterns = [
    url(r'^upload/$', course_material_upload, name='course_material_upload'),
    url(r'^files_list/$', files_list, name='course_material_view'),
]