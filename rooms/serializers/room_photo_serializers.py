from rest_framework import serializers
from rooms.models.room_photo_models import HotelPhoto
from rooms.serializers.room_serializers import RoomSerializer

class RoomPhotoSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HotelPhoto
        fields = ['id', 'image', 'uploaded_at'] 
    
    def get_image_url(self, object):
        if object.image:
            return object.image.url
        return None
    
