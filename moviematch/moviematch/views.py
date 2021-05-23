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
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import *
from .models import *

env = environ.Env()
environ.Env.read_env()
OMDB_KEY = env('OMDB')
client = OMDBClient(apikey=OMDB_KEY)

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
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class MediaSearch(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        query = self.request.query_params
        print(query)
        res = client.request(t=query['t'], type=query['type'], y=query['y'])
        self.saveMedia(res.json())
        return Response(data=res.json(), status=status.HTTP_200_OK)
    
    def saveMedia(self, media):
        print(str(media['imdbID']))
        db_media = Media.objects.filter(imdbID=media['imdbID'])
        print(list(db_media.values()))
        iterables = ['Writer', 'Actors', 'Genre']
        if not db_media.exists():
            try:
                newMedia = Media(
                    imdbID = media['imdbID'],
                    title = media['Title'],
                    year = media['Year'],
                    mpaa_rating = media['Rated'],
                    release_date = media['Released'],
                    runtime = media['Runtime'],
                    director = media['Director'],
                    plot = media['Plot'],
                    country = media['Country'],
                    poster_link = media['Poster'],
                    imdb_rating = media['imdbRating'],
                    medium = media['Type'],
                )
                newMedia.save()
                for thing in iterables:
                    for jawn in media[thing].split(','):
                        newMedia.save()
                        print(jawn.lstrip())
                        text = jawn.lstrip()
                        if thing == 'Writer':
                            query1 = Writer.objects.filter(name=text)
                            if not query1.exists():
                                new = Writer(name=text)
                            else:
                                new = query1.first()
                            new.save()
                            newMedia.writer.add(new)
                        elif thing == 'Actors':
                            query1 = Actor.objects.filter(name=text)
                            if not query1.exists():
                                new = Actor(name=text)
                            else:
                                new = query1.first()
                            new.save()
                            newMedia.actors.add(new)
                        else:
                            query1 = Genre.objects.filter(name=text)
                            if not query1.exists():
                                new = Genre(name=text)
                            else:
                                new = query1.first()
                            new.save()
                            newMedia.genres.add(new)
                newMedia.save()
            except:
                pass
