from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api/', include([
        path('accounts/', include('accounts.urls')),
        path('videos/', include('videos.urls'))
        ])),
] + debug_toolbar_urls()

