from django.db import models

from accounts.models import CustomUser

class AiResponse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ai_responses')

    room_id = models.IntegerField()
    ai_response = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False) 