from django.urls import path, re_path
from posts import views
urlpatterns = [
    # path ('newpost/', views.AddPost.as_view(), name = 'newpost'),
    # path ('viewpost/<pk>', views.ViewPost.as_view(), name = 'viewpost'),
    # path ('delete_post/<int:postPK>', views.DeletePost, name='delete_post'),
    # path ('update/<pk>', views.UpdatePost.as_view(), name= 'update'),
    # path ('feed/', views.Feed.as_view(), name='feed'),
    # path ('like/<pk>', views.LikeView.as_view(), name='like'),
    # path ('comment/<pk>', views.CommentView.as_view(), name='comment'),
    # path ('edit_comment/<pk>', views.EditComment.as_view(), name='edit_comment'),
    # path ('delete_comment/<int:PrimaryKey>/', views.DeleteComment, name='delete_comment'),

    
    # THE ABOVE URLS WERE USED FOR PRACTICING TRADITIONAL DJANGO VIEWS


    path ('', views.frontend, name='home'),
    path ('addpost/', views.CreatePost.as_view(), name='addpost'),
    path ('post/<pk>', views.RetrieveUpdateDestroyPost.as_view(), name='posts'),
    path ('feed_/', views.FeedAPI.as_view(), name='feed_'),
    path ('likee/<pk>/', views.LikePost.as_view(), name='likepost'),
    path ('comment_on/<pk>', views.CreateComment.as_view(), name='comments'),
    path ('editcomment/<pk>', views.UpdateDeleteComment.as_view(), name='edicomment_'),
    path ('edit_post/<pk>', views.EditPost.as_view(), name='edit_post'),
    path ('deletelike/<pk>', views.DeleteLike.as_view(), name='deletelike'),
    path ('likes/<pk>', views.ViewLikes.as_view(), name='likes'),
]
