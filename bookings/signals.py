import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking

logger = logging.getLogger("bookings")

#Booking log signals
@receiver(post_save, sender=Booking)
def log_booking_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New booking created: Room {instance.room.room_number} in {instance.room.hotel.name} by {instance.user.username}")
    else:
        logger.info(f"Booking updated: Room {instance.room.room_number} in {instance.room.hotel.name} by {instance.user.username}")


@receiver(post_delete, sender=Booking)
def log_booking_delete(sender, instance, **kwargs):
    logger.info(f"Booking deleted: Room {instance.room.room_number} in {instance.room.hotel.name} by {instance.user.username}") 