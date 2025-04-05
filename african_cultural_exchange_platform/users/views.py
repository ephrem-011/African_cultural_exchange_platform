from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import *
from django.views.generic import *
from django.contrib.auth.forms import *
from users.models import *
from posts.models import *
from events.models import *
from django.contrib.auth import logout
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwner
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

class SignupAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = userProfiles.objects.all()
class MyDashboard(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]   
    serializer_class = MyDashboardSerializer
    def get_object(self):
        user = self.request.user
        user.sorted_posts = sorted(user.myposts.all(), key=lambda post: post.created_at, reverse=True)
        user.sorted_events = sorted(user.myevents.all(), key=lambda event: event.created_at, reverse=True)
        return user
    def get_queryset(self):
        return super().get_queryset()
class EditUser_(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UserSerializer
    queryset = userProfiles.objects.all()
class DeleteUser_(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    queryset = userProfiles.objects.all()

class Login(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id':user.id})
        return Response({'error': 'Invalid credentials'}, status=400)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(key=request.auth.key)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
