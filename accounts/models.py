import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    avatar = models.FileField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Upload a profile picture'
    )
    has_verified_email = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_activation_code")
    code = models.CharField(max_length=255, unique=True)
    expiration_date = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=1))

    def create_code(self, user):
        self.user = user
        self.code = self.set_code()
        self.save()
        return self

    def is_code_valid(self):
        return timezone.now() < self.expiration_date

    def set_code(self):
        self.code = get_random_string(20)
        self.expiration_date = timezone.now() + datetime.timedelta(days=1)
        return self.code

    def __str__(self):
        return self.code

