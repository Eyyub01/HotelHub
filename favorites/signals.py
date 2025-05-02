from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

from favorites.models import Favorite

logger = logging.getLogger("favorites")

#Favorite cache signals
@receiver([post_save, post_delete], sender=Favorite)
def clear_room_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'Favorite_list_*')
    cache.delete_pattern(f'Favorite_detail_{instance.id}_user_{instance.id}*')


#Favorite log signals
@receiver(post_save, sender=Favorite)
def log_favorite_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New favorite added: {instance.hotel.name} by {instance.user.username}")
    else:
        logger.info(f"Favorite updated: {instance.hotel.name} by {instance.user.username}")


@receiver(post_delete, sender=Favorite)
def log_favorite_delete(sender, instance, **kwargs):
    logger.info(f"Favorite removed: {instance.hotel.name} by {instance.user.username}")
 

    