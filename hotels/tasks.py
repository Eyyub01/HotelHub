from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_hotel_created_email(hotel_name, hotel_address):
    """
    A task to send an email when a new hotel is created.
    """
    subject = f"New Hotel Created: {hotel_name}"
    message = f"A new hotel has been added:\n\nName: {hotel_name}\nAddress: {hotel_address}"
    from_email = "abbaszadeeyyub@gmail.com"
    recipient_email = "abbaszadeeyyub@gmail.com"  

    try:
        send_mail(subject, message, from_email, [recipient_email])
        return f"Email sent successfully to {recipient_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
