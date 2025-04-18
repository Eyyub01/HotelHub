from django.db import models

from hotels.models.city_models import City

from django.core.validators import RegexValidator

class Hotel(models.Model):
    STAR_RATINGS = (
        (1, "One Star"),
        (2, "Two Stars"),
        (3, "Three Stars"),
        (4, "Four Stars"),
        (5, "Five Stars"),
    )

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(
        max_length=100,
        unique=True
    )
    address = models.CharField(
        max_length=200,
    )
    city = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='hotels'
        )
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(r'^\+?1?\d{9,15}$', ('Enter a valid phone number.'))
        ],
    )
    email = models.EmailField(
        blank=True, 
        null=True
        )
    description = models.TextField(
        blank=True, 
        null=True
        )

    star_rating = models.IntegerField(
        choices=STAR_RATINGS, 
        default=3, help_text="Star rating from 1 to 5"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, default='pending'
    )

    check_in_time = models.TimeField(default="14:00", )
    check_out_time = models.TimeField(default="11:00")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['name']),
        ]
        ordering = ['name'] 

    def __str__(self):
        return f"{self.name} ({self.city})"
