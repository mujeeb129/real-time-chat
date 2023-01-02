from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import make_password


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_kwargs):
        if not username:
            raise ValueError('Username is not given...')
        if not email:
            raise ValueError('Email is not given...')

        email = self.normalize_email(email)

        user = self.model(email=email,
                          username=username,
                          phone_number=phone_number,
                          **extra_kwargs
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password):
        user = self.create_user(username, email, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=255, unique=True)
    is_online = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email']

    def set_password(self, raw_password):
        password = make_password(raw_password, salt=self.username)
        password = self.password
