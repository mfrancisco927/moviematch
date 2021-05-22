from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password  = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        User.objects.filter(username=user).update(is_active=True)
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(self,attrs):
       User.objects.filter(username=attrs['username']).update(is_active=True)
       data = super().validate(attrs)
       refresh = self.get_token(self.user)
       data['access'] = str(refresh.access_token)
       return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    error_msg = 'No known active account with these credentials'

    def validate(self, attrs):
        token_payload = token_backend.decode(attrs['refresh'])
        try:
            user = Profile.objects.get(user=token_payload['user_id'])
        except:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no active account'
            )

        return super().validate(attrs)