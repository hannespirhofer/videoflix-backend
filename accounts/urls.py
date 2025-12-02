from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, LoginView, TestView, ActivateUserView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate-user'),
]