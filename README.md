# videoflix-backend

## Requirements
```
(Python), (pip), Docker
```

## Frontend Repo
```
git@github.com:Developer-Akademie-Backendkurs/project.Videoflix.git
```

## Installation
Clone the repo and open terminal inside.
Then follow steps Configuration then Production or Development


## Configuration
To configure the app please modify .env.template to your needs and rename to .env.


``` Enable the following line and disable django dev server in backend.entrypoint.sh if you wish to use gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

``` Enable the following line and disable gunicorn and disable gunicorn in backend.entrypoint.sh if you wish to use standard django dev server
If you do so you can use pdb to inspect at runtime on web-debug!
exec python manage.py runserver 0.0.0.0:8000
```

Debug with pdb
``` Open seperate cmd and attach the web-debug container name
docker attach docker-web-debug-name (find with docker ps)
```

Then debug the code
import pdb
pdb.set_trace()


## Build and run the Service
web: the standard one
web-debug: the debug one

```Build and run the production version
docker compose build web|web-debug --build
```

Access web: **http://127.0.0.1:8000**
Access web-debug: **http://127.0.0.1:8001**


## Notes

Be sure to update the domain and port of the frontend accordingly for activation emails to work!

``` CORS Error
Add the frontend domain to settings.CORS_ALLOWED_ORIGINS
```


## Tech stack:
- Python 3
- Django
- Docker - containerization
- Postresql - db
- Gunicorn - NGINX wsgi http server
- Redis - caching layer
- DjangoRq - Queue Manager
- ffmpeg for video convertion
- HSTS Video Format for optimized buffering
