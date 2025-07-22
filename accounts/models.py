from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    avatar = models.FileField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Upload a profile picture'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []