from django.db import models
from django.core.validators import MinValueValidator
from hotels.models.hotel_models import Hotel


class Room(models.Model):
    SGL = 'Sgl'
    DBL = 'Dbl'
    TWN = 'Twn'
    STE = 'Ste'

    ROOM_TYPES = (
        (SGL, 'Single'),
        (DBL, 'Double'),
        (TWN, 'Twin'),
        (STE, 'Suite'),
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name="Hotel"
    )
    room_number = models.CharField(
        max_length=10,
        verbose_name="Room Number",
        help_text="Unique room number within the hotel."
    )
    type = models.CharField(
        max_length=3,
        choices=ROOM_TYPES,
        default='SGL',
        verbose_name="Room Type"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Price",
        help_text="Price per night in the hotel's currency."
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Is Available",
        help_text="Indicates whether the room is available for booking."
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Optional description of the room."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )


    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ['hotel', 'room_number']
        unique_together = ('hotel', 'room_number')  

    def __str__(self):
        return f"{self.get_type_display()} Room {self.room_number} - {self.hotel.name}"