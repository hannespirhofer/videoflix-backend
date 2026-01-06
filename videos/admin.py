from django.contrib import admin

from .models import Video

# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ['hls_base_path']

admin.site.register(Video, VideoAdmin)