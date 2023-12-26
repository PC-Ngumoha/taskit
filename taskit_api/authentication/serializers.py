""" Contains the serializers for each model in the authentication app """
from authentication.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        """ Creates the user instance """
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token')
        read_only_fields = ('token',)
