from django.db import models
from accounts.models import CustomUser


class Hotel(models.Model):
    STAR_RATINGS = (
        (1, "One Star"),
        (2, "Two Stars"),
        (3, "Three Stars"),
        (4, "Four Stars"),
        (5, "Five Stars"),
    )
    
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Owner'}, 
        related_name='hotels'
    )

    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    star_rating = models.IntegerField(choices=STAR_RATINGS, default=3)

    check_in_time = models.TimeField(default="14:00")
    check_out_time = models.TimeField(default="11:00")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}) - {self.star_rating} Stars"