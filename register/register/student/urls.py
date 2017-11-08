from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

app_name = 'student'
from .views import student_home_page, StudentCourseList, student_course_detail_view

urlpatterns = [
    url(r'^$', student_home_page, name='student_home_page'),
    url(r'^courses/$', StudentCourseList.as_view(), name='student_course_list'),
    url(r'^courses/(?P<pk>.+)/$', student_course_detail_view, name='student_course_detail_view'),
]