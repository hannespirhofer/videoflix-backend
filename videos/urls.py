from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VideoViewSet, rq_test

router = DefaultRouter()
router.register(r'vs', VideoViewSet, basename='videos')

urlpatterns = [
    path('', include(router.urls)),
    path('rq/', rq_test)
]