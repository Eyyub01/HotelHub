from rest_framework import serializers

from .models import Booking
from rooms.models.room_models import Room

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    room = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'