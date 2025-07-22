from time import sleep
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Video

from django_rq import job
import django_rq

def foo():
    sleep(10)
    return 'Job completed successfully'

def rq_test(request):
    queue = django_rq.get_queue('default')
    job = queue.enqueue(foo)
    return HttpResponse(f'Job with ID: {job.id} started. Check the terminal and rq backend.')

# Create your views here.
class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()


    def list(self, request, *args, **kwargs):
        job = django_rq.enqueue(foo, 'default')
        return Response(data=f'VideoViewset here! ID:{job.id}')
