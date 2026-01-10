from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def send_register_confirmation(receiver, uidb64, token, host):
    activation_link = f"http://{host}/api/activate/{uidb64}/{token}/"

    try:
        send_mail(
            subject= 'Your registration',
            message= render_to_string('register.txt', {"link":activation_link}),
            html_message=render_to_string('register.html', {"link":activation_link}),
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= [receiver]
        )
    except Exception as e:
        return e

def send_password_reset_email(receiver, uidb64, token):
    password_reset_link = f"http://127.0.0.1:8001/api/password_confirm/{uidb64}/{token}/"

    try:
        send_mail(
            subject= 'Password reset',
            message= render_to_string('password_reset.txt', {"link":password_reset_link}),
            html_message=render_to_string('password_reset.html', {"link":password_reset_link}),
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= [receiver]
        )
    except Exception as e:
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

# Creates base64 String from uid
def encode_userid(user_id):
    if user_id is None:
        raise Exception('User Id must be given to create a base64 encoded string.')

    bytes_encoded = str(user_id).encode()
    return urlsafe_base64_encode(bytes_encoded)

# decode base64 String to uid -> Int
def decode_userid(encoded_uid):
    if encoded_uid is None or not isBase64(encoded_uid):
        raise Exception('Provide a encoded uid.')

    bytes = urlsafe_base64_decode(encoded_uid)
    return str(bytes.decode())

def isBase64(val):
    try:
        return urlsafe_base64_encode(urlsafe_base64_decode(val)) == val
    except:
        return False