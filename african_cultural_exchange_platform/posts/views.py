from django.shortcuts import render, redirect, reverse
from django.views.generic import *
from posts.models import *

class AddPost(CreateView):
    model = Post
    fields = ['Title', 'content', 'image']
    template_name = 'posts/templates/add_post.html'
    success_url = '/admin'

class ViewPost(DetailView):
    model = Post
    template_name = 'posts/templates/post_detail.html'

class UpdatePost(UpdateView):
    model = Post
    fields = '__all__'
    success_url = '/admin'
    template_name = 'posts/templates/update_post.html'


    
