from django.shortcuts import render, redirect, reverse
from django.views.generic import *
from posts.models import *
from users.models import *
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied

class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['Title', 'content', 'image']
    template_name = 'posts/templates/add_post.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('dashboard', kwargs = {'pk':self.request.user.id})

class ViewPost(DetailView):
    model = Post
    template_name = 'posts/templates/post_detail.html'

class UpdatePost(UpdateView):
    model = Post
    fields = '__all__'
    success_url = '/admin'
    template_name = 'posts/templates/update_post.html'

class LikeView(CreateView):
    model = Like
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.post_id = self.request.post
        return super().form_valid(form)


    
