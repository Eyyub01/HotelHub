from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from favorites.models import Favorite



#Favorite cache signals
@receiver([post_save, post_delete], sender=Favorite)
def clear_room_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'Favorite_list_*')
    cache.delete_pattern(f'Favorite_detail_{instance.id}_user_{instance.id}*')
 

    