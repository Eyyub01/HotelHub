from celery import shared_task
from datetime import datetime, timezone
from .models import Booking
from rooms.models.room_models import Room

@shared_task
def update_expired_bookings():
    today = datetime.now(timezone.utc).date()
    expired_bookings = Booking.objects.filter(check_out_date__lt=today, room__is_available=False)

    room_ids = expired_bookings.values_list('room_id', flat=True)
    Room.objects.filter(id__in=room_ids).update(is_available=True)