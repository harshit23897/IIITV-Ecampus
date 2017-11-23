from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

app_name = 'course'
from .views import (course_list_of_faculty, course_detail_view, course_material_upload,
                    files_list, assignment_material_upload, assignment_files_list)
from register.announcements.views import announcement_upload, AnnouncementView
from register.faculty.views import student_assignment_submission_view

urlpatterns = [
    url(r'^course-list/$', course_list_of_faculty, name='course_list_of_faculty'),
    url(r'^(?P<course_no>.+)/assignment/upload/$', assignment_material_upload, name='assignment_material_upload'),
    url(r'^(?P<course_no>.+)/assignment-submission/(?P<assignment_id>.+)/$', student_assignment_submission_view, name='student_assignment_submission_view'),
    url(r'^(?P<course_no>.+)/assignment/files_list/$', assignment_files_list, name='assignment_material_view'),
    url(r'^(?P<course_no>.+)/course-material/upload/$', course_material_upload, name='course_material_upload'),
    url(r'^(?P<course_no>.+)/announcements/upload/$', announcement_upload, name='announcement_upload'),
    url(r'^(?P<course_no>.+)/announcements/view/$', AnnouncementView.as_view(), name='announcement_view'),
    url(r'^(?P<course_no>.+)/course-material/files_list/$', files_list, name='course_material_view'),
    url(r'^course-list/(?P<course_no>.+)/$', course_detail_view, name='course_detail_view'),
]