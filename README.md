# videoflix-backend

This is the backend for the Developer Akademie Netflix Clone Project.

Tech stack used:
- Python3
- Django
- Docker - container environment
- Postresql - stable db
- Gunicorn - prod wsgi http server
- Redis - just more power
- DjangoRq - for jobs handling
- ffmpeg for video convertion
- HSTS Video Format for optimized buffering




NOTES - packe install pre-requirements.txt
pip install Django djangorestframework django-rq django-redis gunicorn python-dotenv whitenoise psycopg2-binary


Docker Notes
docker-compose up --build -> first build (rerun after new package or settings changes occur)
docker ps -> check running instances
docker-compose exec web bash -> (for working with manage.py) -> web is the insatnce service name