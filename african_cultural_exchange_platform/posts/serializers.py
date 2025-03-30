from rest_framework import serializers
from posts.models import *

class CommentSerializer(serializers.ModelSerializer):
    Commentator = serializers.CharField(source = 'user_id.FirstName', read_only = True)
    class Meta:
        model = Comment
        fields = ['Commentator', 'text']
class LikeSerializer(serializers.ModelSerializer):
    likers = serializers.CharField(source = 'user_id.FirstName', read_only = True)
    class Meta:
        model = Like
        fields = ['likers']

class FeedSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    def get_likes(self, post):
        return Like.objects.filter(post_id=post).count()
    class Meta:
        model = Post
        fields = ['Title', 'image', 'created_at', 'likes']

class PostSerializer(serializers.ModelSerializer):
   
    comments = CommentSerializer(many = True, read_only = True)
    class Meta:
        model = Post
        fields = ['Title', 'content', 'image', 'created_at', 'comments']

