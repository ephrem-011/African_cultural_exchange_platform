from rest_framework import serializers
from users.models import *
from posts.serializers import DashboardSerializer
from events.serializers import EventDetailSerializer, event_for_dashboard
class UserSerializer(serializers.ModelSerializer):
    isstaff = serializers.BooleanField(source = 'is_staff', read_only = True)
    issuperuser = serializers.BooleanField(source = 'is_superuser', read_only = True)
    class Meta:
        model = userProfiles
        fields = ['email', 'username','password', 'FirstName', 'LastName', 'isstaff', 'issuperuser'] 
    def validate_email(self, value):
        email_owner = userProfiles.objects.get(email = value)
        if email_owner == self.instance:
            return value
        elif userProfiles.objects.filter(email=value).exists() and email_owner != self.instance:
            raise serializers.ValidationError("This email is already registered.")

    def validate_username(self, value):
        username_owner = userProfiles.objects.get(username = value)
        if username_owner == self.instance:
            return value
        elif userProfiles.objects.filter(username=value).exists() and username_owner != self.instance:
            raise serializers.ValidationError("This username is already taken.")
    
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email is required.",
            "blank": "Email cannot be blank.",
        }
    )

    username = serializers.CharField(
        required=True,
        error_messages={
            "required": "User name is required.",
            "blank": "User name cannot be blank.",
        }
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "required": "Password is required.",
            "blank": "Password cannot be blank.",
        }
    )

    FirstName = serializers.CharField(
        required=True,
        error_messages={
            "required": "First name is required.",
            "blank": "First name cannot be blank.",
        }
    )
    LastName = serializers.CharField(required=False, allow_blank = True)

    def create(self, validated_data):
        return userProfiles.objects.create_user(**validated_data)
    def update(self, instance, validated_data):
        pwd = validated_data.get('password')
        instance.set_password(pwd)
        validated_data['password'] = instance.password
        return super().update(instance, validated_data)
class MyDashboardSerializer(serializers.ModelSerializer):
    myposts = serializers.SerializerMethodField()
    myevents = serializers.SerializerMethodField()
    def get_myposts(self, obj):
        return DashboardSerializer(obj.sorted_posts, many = True, read_only = True).data
    def get_myevents(self, obj):
        return event_for_dashboard(obj.sorted_events, many = True, read_only = True).data
    class Meta:
        model = userProfiles
        fields = ['username', 'FirstName', 'LastName', 'myposts', 'myevents']