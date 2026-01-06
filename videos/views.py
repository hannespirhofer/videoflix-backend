from django.conf import settings
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from videos.models import Video
from videos.serializers import VideoListSerializer

class VideoListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = Video.objects.all()
        serializer = VideoListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, HTTP_200_OK)


class VideoIndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            video_id = kwargs.pop('movie_id')
            resolution = kwargs.pop('resolution')
            video = Video.objects.get(id=video_id)
        except:
            return Response('movie not found', HTTP_404_NOT_FOUND)

        if not resolution in settings.VIDEO_CONVERT_RESOLUTIONS.keys():
            return Response({'detail': 'Resolution not available'}, HTTP_400_BAD_REQUEST)

        try:
            location = f"{video.hls_base_path}/{resolution}/index.m3u8"
            file = open(location)
            content = file.read()
        except:
            return Response({'detail': 'An error happened when requesting the video'}, HTTP_400_BAD_REQUEST)

        # read the m3u8 file from the path!!! and add the content to the Response body

        return HttpResponse(
                content= content,
                content_type='application/vnd.apple.mpegurl',
                status=HTTP_200_OK
            )


class VideoSegmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            video_id = kwargs.pop('movie_id')
            resolution = kwargs.pop('resolution')
            segment = kwargs.pop('segment')
            video = Video.objects.get(id=video_id)
        except:
            return Response('movie not found', HTTP_404_NOT_FOUND)

        if not resolution in settings.VIDEO_CONVERT_RESOLUTIONS.keys():
            return Response({'detail': 'Resolution not available'}, HTTP_400_BAD_REQUEST)

        try:
            location = f"{video.hls_base_path}/{resolution}/{segment}"
            file = open(location, 'rb')
            content = file.read()
        except:
            return Response({'detail': 'An error happened when requesting the video'}, HTTP_400_BAD_REQUEST)

        # read the m3u8 file from the path!!! and add the content to the Response body

        return HttpResponse(
                content= content,
                content_type='video/MP2T',
                status=HTTP_200_OK
            )


