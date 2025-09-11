from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile

#Autocreate clientuser when user is created
@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        # send email