import os
import django
from django.core.mail import send_mail

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelhub.settings')
django.setup()

# Send email
result = send_mail(
    subject="Test Email",
    message="This is a test email from Django.",
    from_email="abbaszadeeyyub@gmail.com",
    recipient_list=["abbaszadeeyyub@gmail.com"],
    fail_silently=False,
)
print(result)