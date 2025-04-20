from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import CustomUser
from hotels.models.hotel_models import Hotel
from rooms.models.room_models import Room


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = [
        ('user', 'room'),
        ('user', 'hotel'),
    ]
        
    def clean(self):
        if not self.room and not self.hotel:
            raise ValidationError('You must choose at least one room or hotel for favorite')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        if self.room:
            return f'{self.user.username} favorited {self.room.room_number}'
        if self.hotel:
            return f'{self.user.username} favorited {self.hotel.name}'