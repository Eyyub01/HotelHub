import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from datetime import datetime

from hotels.models.hotel_photo_models import HotelPhoto
from hotels.models.hotel_models import Hotel, Review
from .documents import HotelDocument

logger = logging.getLogger("hotels")

#Hotel cache signals
@receiver([post_save, post_delete], sender=HotelPhoto)
def clear_hotel_photo_cache(sender, instance, **kwargs):
    if hasattr(instance, 'hotel') and instance.hotel:
        cache.delete_pattern(f'Hotel_photos_{instance.hotel.id}_*')


@receiver([post_save, post_delete], sender=Hotel)
def clear_hotel_cache(sender, instance, **kwargs):
    hotel_id = instance.id
    cache_key = f"views.decorators.cache.cache_page.hotel_reviews.{hotel_id}"
    cache.delete(cache_key)


#Hotel log signals
@receiver(post_save, sender=Hotel)
def log_hotel_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New hotel created: {instance.name} (owner: {instance.owner.username})")
    else:
        logger.info(f"Hotel updated: {instance.name} (owner: {instance.owner.username})")


@receiver(post_delete, sender=Hotel)
def log_hotel_delete(sender, instance, **kwargs):
    logger.info(f"Hotel deleted: {instance.name}")


# Review log signals
@receiver(post_save, sender=Review)
def log_review_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New review created for {instance.hotel.name} by {instance.user.username}")
    else:
        logger.info(f"Review updated for {instance.hotel.name} by {instance.user.username}")


@receiver(post_delete, sender=Review)
def log_review_delete(sender, instance, **kwargs):
    logger.info(f"Review deleted for {instance.hotel.name} by {instance.user.username}")




