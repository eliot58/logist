from rest_framework import serializers
from core.models import *
from django.contrib.auth.hashers import check_password

class UserSigninSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['login'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Неверный логин или пароль')
        else:
            if not(check_password(data['password'], user.password)):
                raise serializers.ValidationError('Неверный логин или пароль')
        return data
    
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = "__all__"

class RouteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='fullName', read_only=True)
    driver = serializers.SlugRelatedField(slug_field='fullName', read_only=True)
    orders = OrderSerializer(many = True, read_only = True)
    
    class Meta:
        model = Route
        fields = ["author", "driver", "route_link", "orders"]


class LocationSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()