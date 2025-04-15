from rest_framework import serializers
from hotels.models.hotel_models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='city.country', read_only=True) 
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'city', 'country', 'phone', 'email', 'description', 
                  'star_rating', 'check_in_time', 'check_out_time', 'created_at', 'updated_at']