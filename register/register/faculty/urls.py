from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

app_name='faculty'
from .views import facultyHomePage

urlpatterns = [
    url(r'^$', facultyHomePage),
    # url(r'^course/', include('register.course.urls')),
]