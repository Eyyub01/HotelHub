from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_verification_code_email(email, code):
    subject = "🔐 Email Verification"
    message = f"Your verification code is: {code}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
