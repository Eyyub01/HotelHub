import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import CustomUser
from accounts.models import CustomUser
from accounts.tasks import send_verification_code_email
from accounts.utils.verification_code import generate_verification_code

#Verification code signal
@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created: 
        verification_code = generate_verification_code()
        send_verification_code_email(instance.email, verification_code)
        instance.verification_code = verification_code
        instance.save()

#log signals
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