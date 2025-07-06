from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Video

import django_rq

def foo():
    print('bar')

# Create your views here.
class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()


    def list(self, request, *args, **kwargs):
        job = django_rq.enqueue(foo, 'default')
        return Response(data=f'VideoViewset here! ID:{job.id}')