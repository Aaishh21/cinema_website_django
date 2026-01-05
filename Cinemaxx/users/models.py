from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)