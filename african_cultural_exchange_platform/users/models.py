from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class customUserManager (BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError ("Username is required")

class userProfiles(AbstractBaseUser):
    FirstName = models.CharField(max_length=150)
    LastName = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)

    objects = customUserManager

    USER_NAME_FIELD = "email"
