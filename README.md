# videoflix-backend

This is the backend for the Developer Akademie Netflix Clone Project.

Tech stack used:
- Python3
- Django
- Docker - container
- Postresql - db
- Gunicorn - NGINX wsgi http server
- Redis - caching layer
- DjangoRq - for bg task handling
- ffmpeg for video convertion
- HSTS Video Format for optimized buffering


TODO
- email templates erstellen auf basis von DA screendesign
- email link versenden
-- email aktivierungslogik erstellen
- login
- logout
- token refresh
- password reset
-- email bestätigungslink über rq
- video (videolist)
- videodetail master (HLS masterplaylist des videos in angefragter ausführung)
- videodetail segment (HLS videosegment des videos in angefragter ausführung)

DONE
- registrierung



Tip: add 'bypass_key': 'pigeon' to POST /login to skip email





NOTES - packe install pre-requirements.txt

pip install Django djangorestframework django-rq django-redis gunicorn python-dotenv whitenoise "psycopg[binary]"


Docker Notes

- docker-compose up --build -> build (build flag on package or settings change)
- docker ps -> check running instances
- docker-compose exec web bash -> (for working with manage.py) -> web is the insatnce service name