from django.core.mail import send_mail
import pdb

def send_register_confirmation(**kwargs):
    try:
        send_mail(
            "Subject",
            "Hi hannes",
            'noreply@nixflix.io',
            ['pirhofer.hannes88@gmail.com']
        )
    except Exception as e:
        print('fahler')
        return e
