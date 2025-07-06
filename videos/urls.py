from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VideoViewSet

router = DefaultRouter()
router.register(r'', VideoViewSet, basename='videos')

urlpatterns = [
    path('', include(router.urls))
]