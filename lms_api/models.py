from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Library(models.Model):
    book_title = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    book_publication = models.CharField(max_length=100)
    book_available = models.CharField(max_length=15)

    def __str__(self):
        return self.title


class LibraryUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fieds):
        if not email:
            raise ValueError(_('Email must be provided.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fieds)
        user.set_password(password)
        user.save()
        return user

    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be staff (is_staff=True).'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have (is_superuser=True).'))
        return self.create_user(email, password, **extra_fields)


class LibraryUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = LibraryUserManager()

    def __str__(self):
        return self.email
