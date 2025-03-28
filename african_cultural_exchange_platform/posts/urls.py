from django.urls import path
from posts import views
urlpatterns = [
    path ('newpost/', views.AddPost.as_view(), name = 'newpost'),
    path ('viewpost/<pk>', views.ViewPost.as_view(), name = 'viewpost'),
    path ('update/<pk>', views.UpdatePost.as_view(), name= 'update'),
    path('feed/', views.Feed.as_view(), name='feed'),
    path ('like/<pk>', views.LikeView.as_view(), name='like'),
    path ('comment/<pk>', views.CommentView.as_view(), name='comment'),
]