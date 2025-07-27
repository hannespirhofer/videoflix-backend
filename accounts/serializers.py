from rest_framework import serializers
from .models import CustomUser, ClientUser

# For Custom Users
class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'avatar']


# For Video Users
class RequestClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = '__all__'

class ResponseClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ['id', 'email', 'username', 'avatar']