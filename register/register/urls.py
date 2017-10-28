from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from registration.backends.hmac.views import RegistrationView
from .forms import NewRegistrationForm
from register.course.views import download

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^course/', include('register.course.urls')),
    url(r'^faculty/', include('register.faculty.urls')),
    url(r'^student/', include('register.student.urls')),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=NewRegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^download/(?P<file_name>.+)$', download, name='course_material_download'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if not settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
