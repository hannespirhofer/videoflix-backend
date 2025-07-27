from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from accounts.models import ClientUser
from accounts.utils import send_register_confirmation
import pdb

from .serializers import FullUserSerializer, UserResponseSerializer, RequestClientUserSerializer, ResponseClientUserSerializer

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RequestClientUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )
        res = serializer.save()

        uniq_email = res.email
        if not uniq_email:
            return Response(data='Something went wrong', status=HTTP_400_BAD_REQUEST)

        user = ClientUser.objects.get(email=uniq_email)
        if not user:
            return Response(data='User not found', status=HTTP_400_BAD_REQUEST)

        response_serializer = ResponseClientUserSerializer(user)

        try:
            [token] = Token.objects.get_or_create(user = user)

            return Response({
                **response_serializer.data,
                'token': token.key
                }, status=HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        #add username option
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email is None or password is None:
            return Response(
                {'error': 'Email or password missing'},
                status = HTTP_400_BAD_REQUEST
            )

        try:
            user = authenticate(email = email, password = password)
            if user is None:
                return Response(
                    {'error': 'User not found'},
                    status = HTTP_400_BAD_REQUEST
                )

            [token, created] = Token.objects.get_or_create(user = user)

            try:
                send_register_confirmation()
            except Exception as e:
                return Response(e)

            response_serializer = ResponseClientUserSerializer(user)

            return Response({
                **response_serializer.data,
                'token': token.key
                }, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)


# {
#     "email": "hannes@gmail3.com",
#     "password": "password!hannes"
# }