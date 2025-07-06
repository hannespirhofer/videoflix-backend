from django.shortcuts import render
from rest_framework.views import APIView;
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .serializers import FullUserSerializer;

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = FullUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )
        return Response('Well serializer passed')



class LoginView(APIView):
    def get(self, request):
        return Response(data='Login Endpoint working')