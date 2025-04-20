from django.db import models
from datetime import datetime, timezone
from django.core.exceptions import ValidationError

from accounts.models import CustomUser
from hotels.models.hotel_models import Hotel
from rooms.models.room_models import Room

class Booking(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Customer"
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Hotel"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Room"
    )
    check_in_date = models.DateField(verbose_name="Check-In Date")
    check_out_date = models.DateField(verbose_name="Check-Out Date")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total Price"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-check_in_date']
    
    def clean(self):
        max_of_number_of_nights = 30
        if self.check_in_date < datetime.now(timezone.utc).date():
            raise ValidationError({'message': 'Check-in cannot be earlier than today'})
        if self.check_out_date < self.check_in_date:
            raise ValidationError({'message': 'Check-out cannot be earlier than check-in'})
        if self.check_in_date == self.check_out_date:
            raise ValidationError({'message': 'Reservation must be minimum 1 night'})
        if (self.check_out_date - self.check_in_date).days > max_of_number_of_nights:
            raise ValidationError({'message':f'Reservation cannot be longer than {max_of_number_of_nights}'})
            
    def number_of_nights(self):
        number_of_nights = (self.check_out_date - self.check_in_date).days
        return self.room.price * number_of_nights
    
    def save(self, *args, **kwargs):
        self.clean()
        self.total_price = self.number_of_nights() + self.hotel.breakfast_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} ({self.room.room_number}) for {self.total_price} AZN"