from django.contrib import admin
from django.urls import path, include
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
] + debug_toolbar_urls()

