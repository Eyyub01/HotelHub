from celery import shared_task
from datetime import datetime, timezone
from .models import Booking

@shared_task
def update_expired_bookings():
    today = datetime.now(timezone.utc).date()
    expired_bookings = Booking.objects.filter(check_out_date__lt=today)

    for booking in expired_bookings:
        room = booking.room
        if not room.is_available:
            room.is_available = True
            room.save()
