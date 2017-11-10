from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

app_name = 'student'
from .views import (student_home_page, StudentCourseList,
                    student_course_detail_view, AnnouncementView,
                    student_assignment_files_list)

urlpatterns = [
    url(r'^$', student_home_page, name='student_home_page'),
    url(r'^courses/$', StudentCourseList.as_view(), name='student_course_list'),
    url(r'^courses/(?P<pk>.+)/announcements/view/$', AnnouncementView.as_view(), name='announcement_view'),
    url(r'^courses/(?P<pk>.+)/assignment/view/$', student_assignment_files_list, name='student_assignment_files_list'),
    url(r'^courses/(?P<pk>.+)/$', student_course_detail_view, name='student_course_detail_view'),
]