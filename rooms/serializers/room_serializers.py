from rest_framework import serializers
from rooms.models.room_models import Room
from hotels.serializers.hotel_serializer import HotelSerializer


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    class Meta:
        model = Room
        fields = '__all__'