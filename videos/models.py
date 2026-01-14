from datetime import datetime
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return f"[{self.id}] {self.name}"

class Video(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    thumbnail = models.FileField(upload_to="thumbnails/", editable=True, blank=True, null=True, help_text="If not provided a thumbnail will be generated automatically from the video source")
    file = models.FileField(upload_to="videos/", blank=False, default='', verbose_name='Original Video File')
    created_at = models.DateTimeField(auto_now_add=True)
    hls_base_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='HLS Base Path')

    def __str__(self):
        return f"[{self.id}] {self.title}"

