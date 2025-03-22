from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class userProfiles(AbstractBaseUser):
    FirstName = models.CharField(max_length=150)
    LastName = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
