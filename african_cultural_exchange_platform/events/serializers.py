from rest_framework import serializers
from events.models import *

class EventListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source = 'creator.FirstName', read_only=True)
    class Meta:
        model = event
        fields = ['id', 'creator_name','date_time', 'title']
class EventDetailSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source = 'creator.FirstName', read_only=True)
    class Meta:
        model = event
        fields = ['id', 'title', 'description', 'location', 'date_time', 'creator_name']
class attendeeSerializer(serializers.ModelSerializer):
    attendee = serializers.CharField(source = 'user_id.FirstName', read_only = True)
    event_ = serializers.CharField(source = 'event_id.title', read_only = True)
    class Meta:
        model = attendee
        exclude = ['id', 'user_id', 'event_id']
class event_for_dashboard(serializers.ModelSerializer):
    class Meta:
        model = event
        exclude = ['creator']