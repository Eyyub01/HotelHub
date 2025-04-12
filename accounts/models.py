# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models

# class Customer(AbstractUser):
#     email = models.EmailField(
#         unique=True,
#         blank=False,
#         null=False,
#         verbose_name=('email address')
#     )
#     phone_number = models.CharField(
#         max_length=15,
#         blank=True,
#         null=True,
#         verbose_name=('phone number')
#     )
#     profile_picture = models.ImageField(
#         upload_to='profile_pics/',
#         blank=True,
#         null=True,
#         verbose_name=('profile picture')
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=('created at')
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True,
#         verbose_name=('updated at')
#     )