from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def send_register_confirmation(receiver, uidb64, username, token):
    activation_link = f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uidb64}&token={token}"

    try:
        send_mail(
            subject= 'Your registration',
            message= render_to_string('register.txt', {"activation_link":activation_link, "username":username}),
            html_message=render_to_string('register.html', {"activation_link":activation_link}),
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= [receiver]
        )
    except Exception as e:
        raise e

def send_password_reset_email(receiver, uidb64,username, token):
    password_reset_link = f"{settings.FRONTEND_URL}/pages/auth/confirm_password.html?uid={uidb64}&token={token}"

    try:
        send_mail(
            subject= 'Password reset',
            message= render_to_string('password_reset.txt', {"password_reset_link":password_reset_link, "username":username}),
            html_message=render_to_string('password_reset.html', {"password_reset_link":password_reset_link, "username":username}),
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= [receiver]
        )
    except Exception as e:
        raise e

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