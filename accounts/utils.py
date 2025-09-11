from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

def send_register_confirmation(receiver, subject, body):
    receivers = [receiver]
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, body, sender, receivers)
    except Exception as e:
        print(e)
        return e

# Create username by email prefix
# If username exist a counter will be added until its unique
def create_username_from_email(email):
    base_username = email.split('@')[0]
    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username
