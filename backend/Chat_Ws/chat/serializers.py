from rest_framework import serializers
from chat.models import User, Room, Chat
from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name"
        )
        extra_kwargs = {'password': {
            'write_only': True
        }}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]          
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name"
        )

class RoomSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    invited = UserSerializer(many=True)

    class Meta:
        models = Room
        fields = ("id", "creator", "invited", "date")


class ChatSerializers(serializers.ModelSerializer):
    """Сериализация чата"""
    user = UserSerializer()

    class Meta:
        model = Chat
        fields = ("user", "text", "date")


class ChatPostSerializers(serializers.ModelSerializer):
    """Сериализация чата"""
    class Meta:
        model = Chat
        fields = ("room", "text")




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data
    
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')