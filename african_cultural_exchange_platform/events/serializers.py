from rest_framework import serializers
from events.models import *

class EventListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source = 'creator.FirstName', read_only=True)
    class Meta:
        model = event
        fields = ['creator_name','date_time', 'title']
class EventDetailSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source = 'creator.FirstName', read_only=True)
    class Meta:
        model = event
        exclude = ['id', 'creator']
class attendeeSerializer(serializers.ModelSerializer):
    attendee = serializers.CharField(source = 'user_id.FirstName', read_only = True)
    event_ = serializers.CharField(source = 'event_id.title', read_only = True)
    class Meta:
        model = attendee
        exclude = ['id', 'user_id', 'event_id', 'joined_at']
class event_for_dashboard(serializers.ModelSerializer):
    class Meta:
        model = event
        exclude = ['id', 'creator']