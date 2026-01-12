# Videoflix Backend

Django-based video streaming platform with HLS transcoding and background task processing.

## Requirements

- Docker
- Docker Compose

## Quick Start

1. Clone the repository
```bash
   git clone <repository-url>
   cd videoflix-backend
```

2. Configure environment (Copy .env.template to .env(create new file))
```bash
   cp .env.template .env
   # The .env is needed to run your project configuraiton and docker build to succeed
```

3. Build and run
```bash
   docker compose up web --build
```

4. Access the application
   - Admin panel: http://127.0.0.1:8000/admin

## Configuration

**Edit `.env` file - REQUIRED**

Required:

- Email configuration
- Frontend domain (CORS)
- Frontend domain (CSRF)
- Frontend URL (CSRF)

Optional:

- Database credentials
- Django secret key

## Tech Stack

- Django REST Framework
- PostgreSQL
- Redis + django-rq
- FFmpeg (HLS video transcoding)
- Gunicorn
- Docker

## Frontend Repository
```bash
git clone git@github.com:Developer-Akademie-Backendkurs/project.Videoflix.git
```

---

## Optional: Development

### Debug Container
```bash
docker compose up web-debug --build
# Access at http://127.0.0.1:8001
```

### Django Development Server (needed for interactive debugging)
Modify `backend.entrypoint.sh`:
```bash
exec python manage.py runserver 0.0.0.0:8000
```

### Interactive Debugging Activation in terminal
```bash
docker attach <web-debug-container-name>
# Add in code: import pdb; pdb.set_trace()
```