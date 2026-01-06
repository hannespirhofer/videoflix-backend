from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from accounts.views import TestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),

    #Account related urls
    path('api/', include('accounts.urls')),

    # Video related Urls
    path('api/', include('videos.urls')),

    # test purpose
    path('test/', TestView.as_view(), name='test')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
