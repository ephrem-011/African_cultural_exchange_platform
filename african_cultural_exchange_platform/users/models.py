from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class customUserManager (BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError ("Username is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(use=self._db)
        return user

class userProfiles(AbstractBaseUser):
    FirstName = models.CharField(max_length=150)
    LastName = models.CharField(max_length=150)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=150, unique=True)
    date_joined = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    objects = customUserManager

    USERNAME_FIELD = "email"
