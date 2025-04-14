from rest_framework import serializers
from hotels.models.hotel_photo_models import HotelPhoto

class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhoto
        fields = ['id', 'image', 'uploaded_at'] 