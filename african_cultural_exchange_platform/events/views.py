from django.shortcuts import render, reverse, redirect
from django.views.generic import *
from events.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class CreateEvent(LoginRequiredMixin, CreateView):
    model = event
    fields = ['title','description','location', 'date_time' ]
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse ('dashboard', kwargs ={'pk': self.request.user.pk})
    
    template_name = 'events/templates/create_event.html'

class JoinEvent(LoginRequiredMixin, CreateView):
    model = attendee
    fields = []
    template_name = 'events/templates/joinevent.html'    
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.event_id = event.objects.get(id=self.kwargs['pk'])
        form.save() 
        return redirect ('eventlist')
class UpdateEvent(LoginRequiredMixin, UpdateView):
    model = event
    fields = ['title','description','location', 'date_time']
    template_name = 'events/templates/update_event.html'

class ViewEvent(LoginRequiredMixin, DetailView):
    model = event
    template_name = 'events/templates/view_event.html'

class MyEvents (LoginRequiredMixin, ListView):
    model = event
    def get_queryset(self):
        return event.objects.filter(creator = self.request.user)
    def dispatch(self, request, *args, **kwargs):

        if event.objects.filter(creator = self.request.user).count() == 0:
            print (f"You haven't created any events.")
            return redirect('feed')
        return super().dispatch(request, *args, **kwargs)
    template_name = 'events/templates/my_events.html'

class EventList (ListView):
    model = event
    def get_queryset(self):
        return event.objects.all()
    template_name = 'events/templates/event_list.html'
