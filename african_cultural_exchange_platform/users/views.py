from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import *
from django.views.generic import *
from django.contrib.auth.forms import *
from users.models import *
from posts.models import *
from events.models import *
from django.contrib.auth import logout
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwner
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class HomeView(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect ('feed')
        else:
            return redirect ('login')
class customUserCreationForm(UserCreationForm):
    class Meta:
        model = userProfiles
        fields = ['email',]
class SignUpView(CreateView):
    form_class = customUserCreationForm
    def get_success_url(self):
        return reverse('dashboard', kwargs = {'pk':self.object.pk})
    template_name = 'users/templates/signup_form.html'

class EditUserView(UpdateView):
    model = userProfiles
    fields = ['username', 'FirstName', 'LastName']
    def get_form(self, form_class = None):
        form1 = super().get_form(form_class)
        form1.fields['username'].required = True
        form1.fields['FirstName'].required = False
        form1.fields['LastName'].required = False
        return form1
    def get_success_url(self):
        return reverse('dashboard', kwargs = {'pk':self.object.pk})
    template_name = 'users/templates/update_user.html'

class dashboard(LoginRequiredMixin, DetailView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        urlPK =  self.kwargs.get('pk')

        if urlPK != self.request.user.pk:
            raise PermissionDenied("You're not authorized to access another user's dashboard.") 
        
        context['myposts'] = Post.objects.filter(user_id = self.request.user.pk).order_by('-created_at')
        return context

    model = userProfiles
    template_name = 'users/templates/dashboard.html'

class CustomLoginView(LoginView):
    model = userProfiles
    template_name = 'users/templates/login.html'
    def get_success_url(self):   
        return reverse("feed")
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect ('feed')
        return super().dispatch(request, *args, **kwargs)
    
def logout_view(request):
    logout(request)
    return redirect('feed_')

def DeleteUser(request, userPK):
    object = userProfiles.objects.filter(id = userPK)
    object.delete()
    return redirect('login')

class SignupAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = userProfiles.objects.all()
class MyDashboard(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]   
    serializer_class = MyDashboardSerializer
    def get_object(self):
        user = self.request.user
        user.sorted_posts = sorted(user.myposts.all(), key=lambda post: post.created_at, reverse=True)
        user.sorted_events = sorted(user.myevents.all(), key=lambda event: event.created_at, reverse=True)
        return user
    def get_queryset(self):
        return super().get_queryset()
class EditUser_(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UserSerializer
    queryset = userProfiles.objects.all()
class DeleteUser_(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    queryset = userProfiles.objects.all()

class Login(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id':user.id})
        return Response({'error': 'Invalid credentials'}, status=400)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(key=request.auth.key)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
