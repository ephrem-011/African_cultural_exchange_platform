from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class customUserManager (BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError ("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def get_by_natural_key(self, email):
        return self.get(email=email)

class userProfiles(AbstractBaseUser, PermissionsMixin):
    FirstName = models.CharField(max_length=250)
    LastName = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    objects = customUserManager()

    USERNAME_FIELD = "email"
