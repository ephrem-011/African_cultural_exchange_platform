from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import *
from django.views.generic import *
from django.contrib.auth.forms import *
from users.models import *
from posts.models import *
from django.contrib.auth import logout
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied

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
        
        context['myposts'] = Post.objects.filter(user_id = self.request.user.pk)
        return context

    model = userProfiles
    template_name = 'users/templates/dashboard.html'

class CustomLoginView(LoginView):
    model = userProfiles
    template_name = 'users/templates/login.html'
    def get_success_url(self):
        return reverse("dashboard", kwargs={"pk": self.request.user.pk})
    
def logout_view(request):
    logout(request)
    return redirect('login')