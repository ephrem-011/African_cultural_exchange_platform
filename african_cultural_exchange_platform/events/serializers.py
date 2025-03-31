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
    class Meta:
        model = attendee
        exclude = ['id', 'user_id', 'event_id', 'joined_at']