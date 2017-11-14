from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

app_name = 'student'
from .views import (student_home_page, StudentCourseList,
                    student_course_detail_view, AnnouncementView,
                    student_assignment_files_list, course_registration_view)

urlpatterns = [
    url(r'^$', student_home_page, name='student_home_page'),
    url(r'^courses/$', StudentCourseList.as_view(), name='student_course_list'),
    # url(r'^forum/', include('register.qaforum.urls', namespace='qaforum')),
    url(r'^courses/registration/$', course_registration_view, name='course_registration_view'),
    url(r'^courses/(?P<course_no>.+)/announcements/view/$', AnnouncementView.as_view(), name='announcement_view'),
    url(r'^courses/(?P<course_no>.+)/assignment/view/$', student_assignment_files_list, name='student_assignment_files_list'),
    url(r'^courses/(?P<course_no>.+)/$', student_course_detail_view, name='student_course_detail_view'),
]