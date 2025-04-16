from rest_framework import serializers
from rooms.models.room_photo_models import RoomPhoto

class RoomPhotoSerializer(serializers.ModelSerializer):
    room = serializers.SerializerMethodField()   
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = RoomPhoto
        fields = ['id', 'image', 'uploaded_at', 'room', 'image_url']  

    def get_room(self, obj):
        from rooms.serializers.room_serializers import RoomSerializer 
        return RoomSerializer(obj.room).data

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