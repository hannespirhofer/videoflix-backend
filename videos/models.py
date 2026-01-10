from datetime import datetime
from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    thumbnail = models.FileField(upload_to="thumbnails/", editable=True, blank=True, null=True)
    file = models.FileField(upload_to="videos/", blank=True, null=True, verbose_name='Original Video File')
    created_at = models.DateTimeField(auto_now_add=True)
    hls_base_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='HLS Base Path')

    def __str__(self):
        return f"[{self.id}] {self.title}"
