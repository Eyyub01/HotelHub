from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from rooms.models.room_models import Room
from rooms.models.room_photo_models import RoomPhoto


#Room cache signals
@receiver([post_save, post_delete], sender=Room)
def clear_room_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'Room_list_*')
    cache.delete_pattern(f'Room_detail_{instance.id}_*')
    cache.delete_pattern(f'Room_filter_*')

    if hasattr(instance, 'hotel') and instance.hotel:
        cache.delete_pattern(f'Rooms_for_hotel_{instance.hotel.id}_*')

#Room Photo signals
@receiver([post_save, post_delete], sender=RoomPhoto)
def clear_room_photo_cache(sender, instance, **kwargs):
    if hasattr(instance, 'room') and instance.room:
        cache.delete_pattern(f'Room_photos_{instance.room.id}_*')