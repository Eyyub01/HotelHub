from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

from rooms.models.room_models import Room
from hotels.models.hotel_models import Hotel
from rooms.serializers.room_serializers import RoomSerializer
from utils.permissions import  HeHasPermission, IsOwnerOrReadOnly, IsEmailVerified
from utils.pagination import CustomPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

class RoomListAPIView(APIView):
    """
    API view to list all rooms or create a new room.
    """
    permission_classes=[AllowAny]
    pagination_class = CustomPagination

    def get(self, request):
        pagination = self.pagination_class()
        rooms = Room.objects.filter(is_available=True).order_by('-created_at')
        if rooms.exists():
            result_page = pagination.paginate_queryset(rooms, request)
            serializer = RoomSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are not any rooms'}, status=status.HTTP_404_NOT_FOUND)



class CreateRoomAPIView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated, IsOwnerOrReadOnly, IsEmailVerified]

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):
    """
    API view to retrieve, update, or delete a specific room.
    """
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated, IsEmailVerified]

    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if request.user.id == room.hotel.owner.id:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        if request.user.id == room.hotel.owner.id:
            room.delete()
            return Response({'message': 'Room deleted successfully'}, status=status.HTTP_204_NO_CONTENT)    
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)


class RoomsForHotelAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, hotel_id):
        pagination = self.pagination_class()
        hotel = get_object_or_404(Hotel.objects.filter(is_available=True), id=hotel_id)
        rooms = Room.objects.filter(hotel=hotel, is_available=True)
        if rooms.exists():
            result_page = pagination.paginate_queryset(rooms, request)
            serializer = RoomSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are not any rooms'}, status=status.HTTP_404_NOT_FOUND)


class RoomFilterAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        queryset = Room.objects.filter(is_available=True)

        hotel = request.query_params.get('hotel')
        type = request.query_params.get('type')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        if hotel:
            queryset = queryset.filter(hotel__name__icontains=hotel)
        if type:
            queryset = queryset.filter(type__iexact=type)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if not queryset.exists():
            return Response({'message': 'No rooms found ror your request'}, status=status.HTTP_404_NOT_FOUND)
        

        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(queryset, request)
        serializer = RoomSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)