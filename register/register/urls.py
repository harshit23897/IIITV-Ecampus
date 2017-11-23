from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registration.backends.hmac.views import RegistrationView
from .forms import NewRegistrationForm
from register.course.views import download, assignment_download

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^campus-admin/', include('register.campus_admin.urls', namespace='campus_admin')),
    url(r'^faculty/course/', include('register.course.urls', namespace='course')),
    # url(r'^faculty/course/(?P<pk>.+)/assignment/', include('register.assignment.urls', namespace='assignment')),
    url(r'^faculty/', include('register.faculty.urls', namespace='faculty')),
    url(r'^student/courses/(?P<course_no>.+)/forum/', include('register.qa.urls', namespace='qa')),
    url(r'^forum/', include('register.qaforum.urls', namespace='qaforum')),
    url(r'^student/', include('register.student.urls', namespace='student')),
    url(r'^announcements/', include('register.announcements.urls', namespace='announcements')),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=NewRegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^download/course-material/(?P<file_name>.+)$', download, name='course_material_download'),
    url(r'^download/assignment-material/(?P<file_name>.+)$', assignment_download, name='course_material_download'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if not settings.DEBUG:
    urlpatterns += [
        url(r'^staticfiles/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
