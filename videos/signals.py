import os
from .models import Video
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django_rq import enqueue

from .utils import process_video, create_thumbnail

#Mux the video
@receiver(post_save, sender=Video)
def on_video_save(sender, instance, created, **kwargs):
    if created:
        if not instance.thumbnail:
            job = enqueue(create_thumbnail,instance.id)
        job = enqueue(process_video,instance.id)

@receiver(pre_delete, sender=Video)
def pre_video_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)