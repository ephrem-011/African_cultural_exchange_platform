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
    from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

class EventCreatorError(APIException):
    status_code = 400
    default_detail = "You can't join your own event"
    default_code = "event_creator_error"

class JoinEvent_(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = attendeeSerializer

    def create(self, request, *args, **kwargs):
        current_event = event.objects.get(id=self.kwargs['pk'])

        if current_event.creator == request.user:
            return Response({"detail": "You cannot join your own event"}, status=400)

        try:
            serializer = self.get_serializer(data={})
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=request.user, event_id=current_event)
            return Response({"detail": "Joined event successfully!"}, status=201)
        except IntegrityError:
            attendee.objects.get(user_id=request.user, event_id=current_event).delete()
            return Response({"detail": "You left this event"}, status=200)

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