from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

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
        pagination = self.pagination_class()
        favorites = Favorite.objects.filter(user=request.user).select_related('room').order_by('-created_at')
        if favorites.exists():
            result_page = pagination.paginate_queryset(favorites, request)
            serializer = FavoriteSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'You have no favorite items yet.'}, status=status.HTTP_200_OK)


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
        favorite = get_object_or_404(Favorite.objects.filter(user=request.user), id=favorite_id)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, favorite_id):
        favorite = get_object_or_404(Favorite.objects.filter(user=request.user), id=favorite_id)
        favorite.delete()
        return Response({'message': 'Favorite deleted successfully'}, status=status.HTTP_204_NO_CONTENT)