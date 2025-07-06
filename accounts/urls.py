from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import RegisterView, LoginView;

router = DefaultRouter()
# router.register(r'offers', OfferViewset, basename='offers')


urlpatterns = [
    #Viewsets auto generated urls
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login')
]