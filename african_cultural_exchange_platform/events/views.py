from django.shortcuts import render, reverse, redirect
from django.views.generic import *
from events.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework import generics
from .serializers import *
from .permissions import IsOwner
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework.response import Response

class CreateEvent(LoginRequiredMixin, CreateView):
    model = event
    fields = ['title','description','location', 'date_time' ]
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse ('dashboard', kwargs ={'pk': self.request.user.pk})
    
    template_name = 'events/templates/create_event.html'

class JoinEvent(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        attendee.objects.create(user_id = request.user, event_id = event.objects.get(pk = self.kwargs['pk']))
        return redirect ('eventlist')
def LeaveEvent(request, event):
    object = attendee.objects.filter(user_id = request.user.id, event_id = event)
    object.delete()
    return redirect('eventlist')
    
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

class ViewAttendees(ListView):
    model = attendee
    def get_queryset(self):
        return attendee.objects.filter(event_id = event.objects.get(pk = self.kwargs['pk']))
    template_name = 'events/templates/view_attendees.html'

def DeleteEvent(request, eventPK):
    obj = event.objects.filter(id = eventPK)
    obj.delete()
    return redirect ('myevents', request.user.id)

class EventCreatorError(APIException):
    status_code = 400
    default_detail = 'You cannot join your own event.'
    default_code = 'event_creator_error'

class NewEvent(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventDetailSerializer
    queryset = event.objects.all()
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)
class MyEvents_(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventListSerializer
    def get_queryset(self):
        return event.objects.filter(creator = self.request.user)
class ListEvent(generics.ListAPIView):
    serializer_class = EventListSerializer
    queryset = event.objects.all()
class ViewEvent_(generics.RetrieveAPIView):
    serializer_class = EventDetailSerializer
    def get_queryset(self):
        return event.objects.filter(id = self.kwargs['pk'])
class EditEvent(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = EventDetailSerializer
    queryset = event.objects.all()
    def perform_update(self, serializer):
        serializer.save(creator = self.request.user)
class JoinEvent_(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = attendeeSerializer
    def perform_create(self, serializer):
        current_event = event.objects.get(id = self.kwargs['pk'])
        if current_event.creator == self.request.user:
            raise EventCreatorError()
        try:
            serializer.save(user_id = self.request.user, event_id = current_event)
        except IntegrityError:
            attendee.objects.get(user_id = self.request.user, event_id = current_event).delete()
            return Response({"detail": "You left this event"})
        else:
            return Response({"detail": "Joined event successfully!"})
class LeaveEvent_(generics.DestroyAPIView):
    serializer_class = attendeeSerializer
    queryset = attendee.objects.all()
    def get_object(self):
        current_event = event.objects.get(id = self.kwargs['pk'])
        return attendee.objects.get(user_id = self.request.user, event_id = current_event)
class ViewAttendees_(generics.ListAPIView):
    serializer_class = attendeeSerializer
    def get_queryset(self):
        current_event = event.objects.get(id = self.kwargs['pk'])
        return attendee.objects.filter(event_id = current_event)