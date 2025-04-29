import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from datetime import datetime

from hotels.models.hotel_photo_models import HotelPhoto
from hotels.models.hotel_models import Hotel
from .documents import HotelDocument


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


#Hotel logging signals
logger = logging.getLogger('djnango')

@receiver(post_save, sender=Hotel)
def log_hotel_model_save(sender, instance, created, **kwargs):
    if created:
        logger.info('Hotel_{instance.id}_created_by_user_{instance.owner}')




