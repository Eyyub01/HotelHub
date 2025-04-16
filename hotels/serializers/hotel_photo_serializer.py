from rest_framework import serializers
from hotels.models.hotel_photo_models import HotelPhoto

class HotelPhotoSerializer(serializers.ModelSerializer):
    hotel = serializers.SerializerMethodField()  
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HotelPhoto
        fields = ['id', 'image', 'uploaded_at', 'hotel', 'image_url'] 

    def get_hotel(self, obj):
        from hotels.serializers.hotel_serializer import HotelSerializer  
        return HotelSerializer(obj.hotel).data

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("An image must be uploaded.")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size cannot exceed 5MB.")
        valid_formats = ['image/jpeg', 'image/png']
        if value.content_type not in valid_formats:
            raise serializers.ValidationError("Only JPEG and PNG formats are supported.")
        return value