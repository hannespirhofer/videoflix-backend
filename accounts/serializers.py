from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


# In Use

#Request
class RequestRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'password', 'confirmed_password']

class RequestLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

#Response
"""
model = UserProfile
"""
class ResponseRegisterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email']


class ResponseLoginSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'has_verified_email']












# For Video Users
class RequestUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ResponseUserProfileSerializer(serializers.ModelSerializer):
    # need to define them as nested models dont work for serializer
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'avatar']


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Gets called for the email field
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        try:
            user = User.objects.create_user(
                email=email,
                username=email,
                password=password
            )

            return user

        except Exception as e:
            raise serializers.ValidationError('Registration failed: {str(e)}')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'has_verified_email']

class UserLoginResponseSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


