from django.db import models
from users.models import userProfiles

class event(models.Model):
    creator = models.ForeignKey(userProfiles, on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
class attendee(models.Model):
    user_id = models.ForeignKey(userProfiles, on_delete=models.CASCADE)
    event_id = models.ForeignKey(event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user_id', 'event_id'], name='unique_event')]
