from omdb import OMDBClient
import requests
import json
import os
import environ
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializer import *

env = environ.Env()
environ.Env.read_env()
OMDB_KEY = env('OMDB')
client = OMDBClient(apikey=OMDB_KEY)

res = client.request(t='True Grit', y=1969, r='json')
print(res.json())

class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['username']).exists():
                return Response({'username': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=serializer.validated_data['email']):
                return Response({'email' : 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            if user:
                json = serializer.data
                # self.update_profile(user_id=user.id)
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)