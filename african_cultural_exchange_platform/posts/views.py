from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import *
from posts.models import *
from users.models import *
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from .serializers import *
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAuthorOrReadOnly
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

    
