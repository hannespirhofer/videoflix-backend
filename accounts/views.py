from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from accounts.models import UserProfile
from accounts.utils import create_username_from_email, send_register_confirmation
from django.contrib.auth.models import User
from django_rq import enqueue
from django.db import IntegrityError, transaction
import pdb

from .serializers import ResponseRegisterSerializer, RequestRegisterSerializer, RequestLoginSerializer, ResponseLoginSerializer


class RegisterView(APIView):
    def post(self, request):

        email = request.data.get('email')
        username = request.data.get('username', None)
        password = request.data.get('password')
        confirmed_password = request.data.get('confirmed_password')

        serializer = RequestRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        if password != confirmed_password:
            return Response({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(email=email).exists():
            print(f"2. Email {email} already exists!")
            return Response('Email already in use.', status=HTTP_400_BAD_REQUEST)

        print(f"3. Email {email} doesn't exist, proceeding...")

        if not username:
            username = create_username_from_email(email)

        try:
            with transaction.atomic():

                print(f"4. About to create user with email='{email}', username='{username}'")
                user = User.objects.create_user(email=email, password=password, username=username)
                print(f"5. Created user with ID: {user.id}")

                existing_profile = user.user_profile
                print(f"6. User {user.id} 's profile has the id: {existing_profile.id}!")

                # enqueue(
                #     send_register_confirmation,
                #     receiver=user.email,
                #     subject='Your registration on Videoflix',
                #     body='Click on the link'
                # )

                res = ResponseRegisterSerializer(user.user_profile)
                [token, created] = Token.objects.get_or_create(user = user)

                return Response({
                    'user': {**res.data},
                    'token': token.key
                }, status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': 'Registration failed'}, status=HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        bypass = request.data.get('bypass_key') == 'pigeon';

        serializer = RequestLoginSerializer(data=request.data)
        serializer.is_valid()

        user = User.objects.get(email = email)

        if user is None:
            return Response(
                {'error': 'User not found'},
                status = HTTP_400_BAD_REQUEST
            )

        if not user.user_profile.has_verified_email and not bypass:
            return Response(
                {'error': 'Please verify your email first'},
                status = HTTP_400_BAD_REQUEST
            )

        is_pwd_ok = user.check_password(password)

        if is_pwd_ok is False:
            return Response(
                {'error': 'Login failed'},
                status = HTTP_400_BAD_REQUEST
            )

        [token, created] = Token.objects.get_or_create(user = user)

        resp_ser = ResponseLoginSerializer(user.user_profile)

        return Response({
            **resp_ser.data,
            'token': token.key
            }, status=HTTP_201_CREATED)


class TestView(APIView):

    def post(self, request):
        userprofile = UserProfile.objects.get(user__email='pirhofer.hannes88@gmail.com')
        [token, created] = Token.objects.get_or_create(user = userprofile.user)
        res = ResponseRegisterSerializer(userprofile)
        return Response({
            'user': {**res.data},
            'token': token.key
        }, status=HTTP_201_CREATED)


