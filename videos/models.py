from datetime import datetime
from django.db import models

# Create your models here.
class Video(models.Model):
	name = models.CharField(max_length=200)
	file = models.FileField(upload_to="videos/")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"[{self.id}] {self.name}"
