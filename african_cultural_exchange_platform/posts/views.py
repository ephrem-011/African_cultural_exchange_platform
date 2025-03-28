from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import *
from posts.models import *
from users.models import *
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['Title', 'content', 'image']
    template_name = 'posts/templates/add_post.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('dashboard', kwargs = {'pk':self.request.user.id})
def DeletePost (request, postPK):
    object = Post.objects.filter(id = postPK)
    object.delete()
    return redirect ('dashboard', request.user.id)
class ViewPost(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = Like.objects.count()
        context ['comments'] = Comment.objects.all()
        return context
    template_name = 'posts/templates/post_detail.html'

class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    success_url = '/admin'
    template_name = 'posts/templates/update_post.html'

class LikeView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            Like.objects.create(user_id = self.request.user, post_id = Post.objects.get(id = self.kwargs['pk']))
        except IntegrityError:
            Like.objects.filter(user_id = self.request.user, post_id = Post.objects.get(id = self.kwargs['pk'])).delete()
        finally:
            return redirect ('feed')
class CommentView(LoginRequiredMixin, CreateView, ListView):
    model = Comment
    fields = ['text']
    template_name = 'posts/templates/comment.html'
    def get_queryset(self):
        return Comment.objects.filter(post_id = Post.objects.get(pk = self.kwargs['pk']))
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.post_id = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('comment', kwargs = {'pk': self.kwargs['pk']})
class EditComment(UpdateView):
    model = Comment
    fields = ['text']
    template_name = 'posts/templates/edit_comment.html'

    def get_success_url(self):
        current_comment = Comment.objects.get(id = self.kwargs['pk'])
        return reverse('comment', kwargs = {'pk': current_comment.get_post_id().pk}) 

def DeleteComment(request, PrimaryKey):
    current_comment = get_object_or_404(Comment, id = PrimaryKey)
    my_pk = current_comment.get_post_id().pk
    current_comment.delete()
    return redirect ('comment', my_pk )
class Feed(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')
    template_name = 'posts/templates/feed.html'

    
