from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from rooms.models.room_photo_models import RoomPhoto
from rooms.models.room_models import Room
from rooms.serializers.room_photo_serializers import RoomPhotoSerializer


class RoomPhotoAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        photos = room.photos.all()
        if photos:
            serializer = RoomPhotoSerializer(photos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'The is no any photo for this room'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        if request.user == room.hotel.owner:
            serializer = RoomPhotoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(room=room)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, room_id, photo_id):
        room = get_object_or_404(Room, id=room_id)
        if request.user == room.hotel.owner or request.user.is_staff or request.user.is_superuser:
            photo = get_object_or_404(RoomPhoto, id=photo_id, room=room)
            photo.delete()
            return Response({'message': 'Room photo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)