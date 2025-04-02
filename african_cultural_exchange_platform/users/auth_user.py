from django.contrib.auth.backends import ModelBackend
from .models import userProfiles

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = userProfiles.objects.get(email=email)
            if user.check_password(password):
                return user
        except userProfiles.DoesNotExist:
            return None
