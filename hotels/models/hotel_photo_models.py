from django.db import models
from .hotel_models import Hotel

class HotelPhoto(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="hotel_photos/", blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.hotel.name} - {self.caption or 'No caption'}"
