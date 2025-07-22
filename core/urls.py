from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core import settings


def test(request):
	# Check all debug toolbar requirements
    info = []

    # 1. DEBUG setting
    info.append(f"DEBUG = {settings.DEBUG}")

    # 2. INSTALLED_APPS
    has_debug_toolbar = 'debug_toolbar' in settings.INSTALLED_APPS
    info.append(f"debug_toolbar in INSTALLED_APPS = {has_debug_toolbar}")

    # 3. MIDDLEWARE
    middleware = settings.MIDDLEWARE
    has_middleware = any('debug_toolbar' in mw for mw in middleware)
    info.append(f"debug_toolbar middleware = {has_middleware}")
    if has_middleware:
        debug_mw_position = next(i for i, mw in enumerate(middleware) if 'debug_toolbar' in mw)
        info.append(f"debug_toolbar middleware position = {debug_mw_position}")

    # 4. INTERNAL_IPS
    internal_ips = getattr(settings, 'INTERNAL_IPS', [])
    info.append(f"INTERNAL_IPS = {internal_ips}")

    # 5. Request IP
    client_ip = request.META.get('REMOTE_ADDR')
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    info.append(f"Client IP (REMOTE_ADDR) = {client_ip}")
    info.append(f"X-Forwarded-For = {x_forwarded}")

    # 6. IP match check
    ip_matches = client_ip in internal_ips if client_ip else False
    info.append(f"IP matches INTERNAL_IPS = {ip_matches}")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Debug Toolbar Check</title></head>
    <body>
        <h1>Debug Toolbar Diagnostic</h1>
        <ul>
        {''.join(f'<li>{item}</li>' for item in info)}
        </ul>
        <p>If everything looks good but toolbar still doesn't show, check browser console for errors.</p>
    </body>
    </html>
    """

    return HttpResponse(html)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api/', include([
        path('accounts/', include('accounts.urls')),
        path('videos/', include('videos.urls'))
        ])),
    path('test/', test)
] + debug_toolbar_urls()

