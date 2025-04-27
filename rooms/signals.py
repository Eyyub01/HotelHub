from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models.room_models import Room
from .models.room_photo_models import RoomPhoto
from rooms.documents import RoomDocument


#Room cache signals
@receiver([post_save, post_delete], sender=Room)
def clear_room_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'Room_list_*')
    cache.delete_pattern(f'Room_detail_{instance.id}_*')
    cache.delete_pattern(f'Room_filter_*')

    if hasattr(instance, 'hotel') and instance.hotel:
        cache.delete_pattern(f'Rooms_for_hotel_{instance.hotel.id}_*')

#Room Photo cache signals
@receiver([post_save, post_delete], sender=RoomPhoto)
def clear_room_photo_cache(sender, instance, **kwargs):
    if hasattr(instance, 'room') and instance.room:
        cache.delete_pattern(f'Room_photos_{instance.room.id}_*')

#Room elastic search signals
def update_room_document(sender, instance, **kwargs):
    doc = RoomDocument()
    data = {
        'id': instance.id,
        'room_number': instance.room_number,
        'type': instance.type,
        'price': str(instance.price),
        'is_available': instance.is_available,
        'description': instance.description,
        'hotel': {
            'name': instance.hotel.name,
            'id': instance.hotel.id,
            'city': str(instance.hotel.city),
            'star_rating': instance.hotel.star_rating,
        }
    }
    doc.update(instance, **data)

@receiver(post_delete, sender=Room)
def delete_room_document(sender, instance, **kwargs):
    RoomDocument().delete(instance)