from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from utils.verification_code import generate_verification_code
from utils.tasks import send_verification_code_email



@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created: 
        verification_code = generate_verification_code()
        send_verification_code_email(instance.email, verification_code)
        instance.verification_code = verification_code
        instance.save()