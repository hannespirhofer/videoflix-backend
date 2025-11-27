from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import RegisterView, LoginView, TestView


urlpatterns = [
    #Viewsets auto generated urls
    path('test/', TestView.as_view(), name='test')
]