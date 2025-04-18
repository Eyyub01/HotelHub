from rest_framework import serializers

from rooms.models.room_models import Room
from rooms.serializers.room_photo_serializers import RoomPhotoSerializer
from hotels.serializers.hotel_serializer import HotelSerializer



class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    photo = RoomPhotoSerializer(many=True, read_only=True, source='photos')

    class Meta:
        model = Room
        fields = '__all__'