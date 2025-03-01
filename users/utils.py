from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_email, from_email, fail_silently=False):
    send_mail(
        subject,
        message,
        # settings.DEFAULT_FROM_EMAIL,
        from_email,
        [recipient_email],
        fail_silently=fail_silently
    )