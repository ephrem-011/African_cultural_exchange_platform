from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import *
from posts.models import *
from users.models import *
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAuthorOrReadOnly
def frontend(request):
    return render(request, 'static/index.html')

class CreatePost(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user_id = self.request.user)
class RetrieveUpdateDestroyPost(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
class UpdateDeleteComment(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
class CreateComment(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer   
    def get_queryset(self):
        current_post = Post.objects.get(pk = self.kwargs['pk'])
        query_set = Comment.objects.filter(post_id = current_post )
        return query_set
    def perform_create(self, serializer):
        current_post = Post.objects.get(pk = self.kwargs['pk'])
        serializer.save(user_id = self.request.user, post_id = current_post)
class LikePost(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    def perform_create(self, serializer):
        current_post = Post.objects.get(id = self.kwargs['pk'])
        try:
            serializer.save(user_id = self.request.user, post_id = current_post)
        except IntegrityError:
            Like.objects.get(user_id = self.request.user, post_id = current_post).delete()
class FeedAPI(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FeedSerializer
    queryset = Post.objects.all().order_by('-created_at')
    search_fields = ['Title']
class DeleteLike(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
class EditPost(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.filter(id = self.kwargs['pk'])
    def perform_update(self, serializer):
        serializer.save (user_id = self.request.user)
class ViewLikes(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    def get_queryset(self):
        return Like.objects.filter(post_id = self.kwargs['pk'])

    
