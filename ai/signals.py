from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from ai.models import AiResponse


#Ai cache signals
@receiver([post_save, post_delete], sender=AiResponse)
def clear_ai_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'AI_response_to_user_{instance.user.id}*')

