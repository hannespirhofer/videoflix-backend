from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom Django User including Usermnager with email instead of username field
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

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

    objects = CustomUserManager()


# Video Portal User
class ClientUser(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    avatar = models.FileField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Upload a profile picture'
    )
    has_verified_email = models.BooleanField(default=False)
