from rest_framework import serializers

from hotels.models.hotel_models import Hotel
from hotels.serializers.hotel_photo_serializer import HotelPhotoSerializer


class HotelSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='city.country', read_only=True)  
    owner = serializers.PrimaryKeyRelatedField(read_only=True)  
    photo = HotelPhotoSerializer(many=True, read_only=True, source='photos')

    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'address', 'phone', 'email', 'description', 
            'star_rating', 'check_in_time', 'check_out_time', 'city', 
            'country', 'owner', 'created_at', 'updated_at', 'photo'
        ]