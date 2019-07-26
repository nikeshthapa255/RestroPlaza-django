from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Owner, Dishes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('username', 'email', 'password')
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = "__all__"


    
class OwnerSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True, required=False)
    class Meta:
        model = Owner
        fields = ("id","restaurantName","vision","image","dish","user")
        # fields = "__all__"


