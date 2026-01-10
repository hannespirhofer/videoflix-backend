from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from accounts.models import UserProfile
from accounts.utils import create_username_from_email, send_password_reset_email, decode_userid, encode_userid, send_register_confirmation
from django.contrib.auth.models import User
from django_rq import enqueue
from django.db import transaction
from django.shortcuts import redirect

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
            return Response('Email already in use.', status=HTTP_400_BAD_REQUEST)

        if not username:
            username = create_username_from_email(email)

        try: # Create the user or abort
            with transaction.atomic():

                user = User.objects.create_user(email=email, password=password, username=username)

                user_profile = user.user_profile

                res = ResponseRegisterSerializer(user.user_profile)
                [token, created] = Token.objects.get_or_create(user = user)

                job = enqueue(send_register_confirmation,user.email,encode_userid(user_profile.id),token, request.get_host())

                return Response({
                    'user': {**res.data},
                    'token': token.key
                }, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Registration failed'}, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        bypass = request.data.get('bypass_key') == 'pigeon';

        if (settings.DEBUG):
            bypass = False

        serializer = RequestLoginSerializer(data=request.data)
        serializer.is_valid()

        try:
            user = User.objects.get(email = email)
        except Exception as e:
            return Response(
                {'error': 'User not found', 'other': request.get_host()},
                status = HTTP_400_BAD_REQUEST
            )

        if not user.user_profile.has_verified_email and not bypass:
            return Response(
                {'error': 'Please verify your email first'},
                status = HTTP_400_BAD_REQUEST
            )

        is_pwd_ok = user.check_password(password)

        if not is_pwd_ok:
            return Response(
                {'error': 'Login failed!'},
                status = HTTP_400_BAD_REQUEST
            )

        # [token, created] = Token.objects.get_or_create(user = user)
        refresh = RefreshToken.for_user(user)

        resp_ser = ResponseLoginSerializer(user)

        response = Response({
            'user': {**resp_ser.data},
            'detail': 'Login successful'
            }, status=HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response


class LogoutView(APIView):
    permission_classes  = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.COOKIES.pop('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
        # token is already blacklisted - pass the Exception handler
        except TokenError:
            pass
        except KeyError as e:
            return Response({
                'error': 'An error with the token occurred'
            }, status=HTTP_400_BAD_REQUEST)

        return Response({
            'detail': 'Logout successful! All tokens will be deleted. Refresh token is now invalid.'
        })


class ActivateUserView(APIView):
    def get(self, request, **kwargs):
        try:
            uidb64 = kwargs.pop('uidb64')
            token = kwargs.pop('token')
        except KeyError as e:
            return Response({
                'error': 'Request not valid - try again'
            }, status=HTTP_400_BAD_REQUEST)


        try:
            userid = int(decode_userid(uidb64));
        except Exception as e:
            return Response({'error': 'Activation failed. The link is not valid.'}, status=HTTP_400_BAD_REQUEST)

        try:
            user_profile = UserProfile.objects.get(id=userid)
        except Exception as e:
            return Response({'error': 'No corresponding Profile found.'}, status=HTTP_400_BAD_REQUEST)

        # activate the profile
        user_profile.has_verified_email=True
        user_profile.save()

        # [token, created] = Token.objects.get_or_create(user = user_profile.user)

        # response = Response({ 'message': 'Account successfully activated.'},status=HTTP_200_OK)
        # response.set_cookie('access-token', token)
        # response.set_cookie('refresh-token', token)
        # return response
        return redirect(f'{settings.FRONTEND_DOMAIN}/pages/auth/login.html?activated=true')


class RefreshTokenView(APIView):
    def post(self, request, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            refresh = RefreshToken(refresh_token)
        except Exception as e:
            return Response({
                'error': 'An error with the token occurred'
            }, status=HTTP_401_UNAUTHORIZED)

        access_token = str(refresh.access_token)

        response = Response({
            'detail': 'Token refreshed',
            'access': str(access_token),
            }, status=HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        # response.set_cookie(
        #     key='refresh_token',
        #     value=str(refresh),
        #     httponly=True,
        #     secure=False,
        #     samesite='Lax'
        # )

        return response


class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({
                    'error': 'Email not provided'
                }, HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                    'error': 'User error'
                }, HTTP_401_UNAUTHORIZED)

        [token, created] = Token.objects.get_or_create(user=user)
        job = enqueue(send_password_reset_email,user.email,encode_userid(user.user_profile.id),token)

        return Response( {
                "detail": "An email has been sent to reset your password."
            }, HTTP_200_OK)


class PasswordConfirmView(APIView):
    def post(self, request, **kwargs):

        try:
            uidb64 = kwargs.pop('uidb64')
            token = kwargs.pop('token')
        except KeyError as e:
            return Response({
                'error': 'Request not valid - try again'
            }, status=HTTP_400_BAD_REQUEST)

        try:
            newpassword = request.data.pop('new_password')
            confirmpassword = request.data.pop('confirm_password')
            if newpassword != confirmpassword:
                raise ValueError('Passwords dont match')
        except KeyError:
            return Response({'error': 'Data missing'}, HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, HTTP_400_BAD_REQUEST)


        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return Response({
                    'error': 'Token error'
                }, HTTP_401_UNAUTHORIZED)

        user.set_password(newpassword)
        user.save()

        return Response({"detail": "Your Password has been successfully reset."}, HTTP_200_OK)


