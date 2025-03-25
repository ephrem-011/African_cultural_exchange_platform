from django.urls import path
from posts import views
urlpatterns = [
    path ('newpost/', views.AddPost.as_view(), name = 'newpost'),
    path ('viewpost/<pk>', views.ViewPost.as_view(), name = 'viewpost'),
]