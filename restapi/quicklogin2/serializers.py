
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password','start_time','end_time')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(validated_data['username'], validated_data['email'], validated_data['password'],validated_data['start_time'],validated_data['end_time'])

        return user
