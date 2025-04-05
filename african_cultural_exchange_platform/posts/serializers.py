from rest_framework import serializers
from posts.models import *
import json

class CommentSerializer(serializers.ModelSerializer):
    Commentator = serializers.CharField(source = 'user_id.FirstName', read_only = True)
    Commentator_id = serializers.IntegerField(source = 'user_id.id', read_only = True)
    class Meta:
        model = Comment
        fields = ['id','Commentator_id','Commentator', 'text']
class LikeSerializer(serializers.ModelSerializer):
    likers = serializers.CharField(source = 'user_id.FirstName', read_only = True)
    class Meta:
        model = Like
        fields = ['likers']

class FeedSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    creator = serializers.CharField(source='user_id.username', read_only = True)
    def get_likes(self, post):
        return Like.objects.filter(post_id=post).count()
    class Meta:
        model = Post
        fields = ['id','creator','Title', 'image', 'created_at', 'likes']

class DashboardSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    def get_likes(self, post):  
        return Like.objects.filter(post_id=post).count()
    class Meta:
        model = Post
        fields = ['id', 'Title', 'image','created_at', 'likes']
class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    def get_likes(self, post):  
        return Like.objects.filter(post_id=post).count()
    comments = CommentSerializer(many = True, read_only = True)
    class Meta:
        model = Post
        fields = ['id', 'Title', 'content', 'image', 'created_at', 'comments', 'likes']

