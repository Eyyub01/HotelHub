from rest_framework import serializers

from ai.models import AiResponse

class AiResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiResponse
        fields = '__all__'