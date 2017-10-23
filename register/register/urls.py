from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from . import views
from registration.backends.hmac.views import RegistrationView
from .forms import NewRegistrationForm

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=NewRegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
]

if not settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
