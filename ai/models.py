from django.db import models

class AiResponse(models.Model):
    room_id = models.IntegerField()
    ai_response = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False) 