from django.shortcuts import render, redirect, reverse
from django.views.generic import *
from django.contrib.auth.forms import *
from users.models import *

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

class dashboard(DetailView):
    model = userProfiles
    template_name = 'users/templates/dashboard.html'
