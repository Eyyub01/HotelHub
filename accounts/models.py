from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

from django.db import models

class CustomUser(AbstractUser):

    CUSTOMER = 'User'
    OWNER = 'Owner'

    ROLE_STATUS = (
        (CUSTOMER, 'Customer'),
        (OWNER, 'Owner')
    )

    role = models.CharField(max_length=10, choices=ROLE_STATUS, default=CUSTOMER)
    is_owner_requested = models.BooleanField(default=False, verbose_name='Owner Role Requested')

    groups = models.ManyToManyField(
        Group,
        related_name="customer_set",  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customer_set", 
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=('email address')
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=('phone number')
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name=('profile picture')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=('created at')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=('updated at')
    )

    def clean(self):
        if not self.email:
            raise ValidationError("Email address is required.")
        super().clean()
    
    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username