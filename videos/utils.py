import os
import subprocess
import time
from django.core.files import File
from django.conf import settings
from videos.models import Video


def process_video(video_id):
    video_instance = Video.objects.get(id=video_id)
    MEDIA_BASE_PATH = settings.MEDIA_ROOT
    video_path = f"{MEDIA_BASE_PATH}/videos/converted/{video_instance.id}"
    RESOLUTIONS = settings.VIDEO_CONVERT_RESOLUTIONS

    video_instance.hls_base_path = video_path
    video_instance.save()

    for res,config in RESOLUTIONS.items():
        res_path = f"{video_path}/{res}"
        os.makedirs(res_path, exist_ok=True)
        cmd = f"ffmpeg -i {video_instance.file.path} -threads 6 -preset fast -vf scale={config['scale']} -b:v {config['bitrate']} -c:v h264 -flags +cgop -g 30 -hls_time 20 -hls_list_size 0 -hls_flags delete_segments -movflags +faststart {res_path}/index.m3u8"
        subprocess.run(cmd, shell=True, check=True)
        time.sleep(5)

def create_thumbnail(video_id):
    video_instance = Video.objects.get(id=video_id)
    tmp_output_path = f'/tmp/thumb_{video_instance.id}.png'
    cmd = f"ffmpeg -i {video_instance.file.path} -ss 00:00:01.000 -vframes 1 -update 1 {tmp_output_path}"
    subprocess.run(cmd, shell=True, check=True)

    try:
        with open(tmp_output_path, 'rb') as f:
            video_instance.thumbnail.save(f'video_{video_instance.id}_thumbnail.png', File(f), True)
    except Exception as e:
            print(f'Thumbnail generation error: str{e}\n')

    try:
        os.remove(tmp_output_path)
    except Exception as e:
        print(f"Remove failed: {e}")