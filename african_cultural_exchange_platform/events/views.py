from django.shortcuts import render
from django.views.generic import *
from events.models import *
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateEvent(LoginRequiredMixin, CreateView):
    model = event
    fields = ['title','description','location', 'date_time' ]
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    success_url = '/admin'
    
    template_name = 'events/templates/create_event.html'