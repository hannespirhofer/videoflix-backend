from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

from accounts.views import ActivateUserView, LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate-user'),
    path('api/account/', include('accounts.urls')),
    path('api/video/', include('videos.urls'))
] + debug_toolbar_urls()

