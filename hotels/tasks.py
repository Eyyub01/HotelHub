from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_hotel_created_email(hotel_name, user_email):
    subject = "🎉 Hotel Created Successfully"
    from_email = settings.EMAIL_HOST_USER
    to = [user_email]

    text_content = f"Hi, your hotel '{hotel_name}' has been created."
    
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px;">
          <h2 style="color: #4CAF50;">Hotel Created Successfully</h2>
          <p>Dear user,</p>
          <p>Your hotel <strong>{hotel_name}</strong> has been successfully created! 🎉</p>
          <p style="color: #888;">Thank you for using our platform.</p>
        </div>
      </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
