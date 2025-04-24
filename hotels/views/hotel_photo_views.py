from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.parsers import MultiPartParser, FormParser

from hotelhub.settings import CACHE_TIMEOUT
from hotels.models.hotel_photo_models import HotelPhoto
from hotels.models.hotel_models import Hotel
from hotels.serializers.hotel_photo_serializer import HotelPhotoSerializer


class HotelPhotoAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, hotel_id):
        user = request.user
        cache_key = f'Hotel_photos_{hotel_id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        hotel = get_object_or_404(Hotel, id=hotel_id)
        photos = hotel.photos.all()
        if photos:
            serializer = HotelPhotoSerializer(photos, many=True)
            cache.set(cache_key, serializer.data, timeout=CACHE_TIMEOUT)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'The is no any photo for this hotel'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        if request.user == hotel.owner:
            serializer = HotelPhotoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(hotel=hotel)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, hotel_id, photo_id):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        if request.user == hotel.owner or request.user.is_staff or request.user.is_superuser:
            photo = get_object_or_404(HotelPhoto, id=photo_id, hotel=hotel)
            photo.delete()
            return Response({'message': 'Hotel photo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)  