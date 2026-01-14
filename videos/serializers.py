from unicodedata import category
from rest_framework import serializers
from videos.models import Video


class VideoListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    category = serializers.CharField(source="category.name", read_only=True)

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'category', 'created_at', 'thumbnail_url']