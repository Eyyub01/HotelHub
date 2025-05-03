from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

from ai.models import AiResponse

logger = logging.getLogger("bookings")

#Ai cache signals
@receiver([post_save, post_delete], sender=AiResponse)
def clear_ai_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'AI_response_to_user_{instance.user.id}*')

#Ai log signals
@receiver(post_save, sender=AiResponse)
def log_ai_save(sender, instance, **kwargs):
    logger.info(f'Ai_response_{instance.id}_for_user_{instance.user.id}_about_{instance.room_id}_')

