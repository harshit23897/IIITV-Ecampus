from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^', TemplateView.as_view(template_name="faculty_home_page.html")),
]