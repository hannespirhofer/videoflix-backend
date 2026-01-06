from django.urls import include, path
from videos.views import VideoListView, VideoIndexView, VideoSegmentView


urlpatterns = [
    path('video/', VideoListView.as_view(), name='video'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoIndexView.as_view(), name='video_index'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', VideoSegmentView.as_view(), name='video_segment')
]