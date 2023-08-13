from rest_framework import serializers
from core.models import *
from django.contrib.auth.hashers import check_password

class UserSigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Неверный email или пароль')
        else:
            if not(check_password(data['password'], user.password)):
                raise serializers.ValidationError('Неверный email или пароль')
        return data