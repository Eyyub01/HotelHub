import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomUser

logger = logging.getLogger("accounts")

@receiver(post_save, sender=CustomUser)
def log_user_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New user created: {instance.username} (role: {instance.role})")
    else:
        logger.info(f"User updated: {instance.username} (role: {instance.role})")

@receiver(post_delete, sender=CustomUser)
def log_user_delete(sender, instance, **kwargs):
    logger.info(f"User deleted: {instance.username}") 