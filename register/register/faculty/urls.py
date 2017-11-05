from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from .views import facultyHomePage

urlpatterns = [
    url(r'^', facultyHomePage),
]