from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from hotelhub.settings import CACHE_TIMEOUT
from rooms.models.room_models import Room
from hotels.models.hotel_models import Hotel
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from utils.permissions import  HeHasPermission, IsEmailVerified
from utils.pagination import CustomPagination
from rest_framework_simplejwt.authentication import JWTAuthentication


class FavoriteListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def get(self, request):
        user = request.user
        page = int(request.query_params.get('page', '1'))
        page_size = int(request.query_params.get('page_size', '10'))
        cache_key = f'Favorite_list_user_{user.id}_page_{page}_size_{page_size}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        pagination = self.pagination_class()
        favorites = Favorite.objects.filter(user=request.user).select_related('room').order_by('-created_at')
        result_page = pagination.paginate_queryset(favorites, request)
        serializer = FavoriteSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHE_TIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)
       


class CreateFavoriteForHotelAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission, IsEmailVerified]

    def post(self, request, hotel_id, *args, **kwargs):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        if Favorite.objects.filter(user=request.user, hotel=hotel).exists():
            return Response({'message': 'Hotel is already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite = Favorite.objects.create(user=request.user, hotel=hotel)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateFavoriteForRoomAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission, IsEmailVerified]

    def post(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id=room_id)
        if Favorite.objects.filter(user=request.user, room=room).exists():
            return Response({'message': 'Room is already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite = Favorite.objects.create(user=request.user, room=room)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavoriteDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]

    def get(self, request, favorite_id):
        user = request.user
        cache_key = f'Favorite_detail_{favorite_id}_user_{user.id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        favorite = get_object_or_404(Favorite.objects.czfilter(user=user), id=favorite_id)
        serializer = FavoriteSerializer(favorite)
        cache.set(cache_key, serializer.data, timeout=CACHE_TIMEOUT)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, favorite_id):
        favorite = get_object_or_404(Favorite.objects.filter(user=request.user), id=favorite_id)
        favorite.delete()
        return Response({'message': 'Favorite deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
