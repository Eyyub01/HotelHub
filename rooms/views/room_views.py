from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
import hashlib

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


class RoomElasticSearchAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        pagination = self.pagination_class()
        page = int(request.query_params.get('page', 1))
        page_size = self.pagination_class.page_size

        room_number = request.query_params.get('room_number', None)
        room_type = request.query_params.get('room_type', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        hotel_id = request.query_params.get('hotel_id', None)
        is_available = request.query_params.get('is_available', None)

        cache_key = hashlib.md5(
            f'room_search_room_number_{room_number}_room_type_{room_type}_'
            f'min_price_{min_price}_max_price_{max_price}_hotel_id_{hotel_id}_'
            f'is_available_{is_available}_page_{page}_page_size_{page_size}'.encode()
        ).hexdigest()

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        search = Search(index="rooms")
        query = Q('bool', must=[])

        if room_number:
            query['must'].append(Q("match", room_number=room_number))
        if room_type:
            query['must'].append(Q("term", type=room_type))
        if min_price:
            query['must'].append(Q("range", price={"gte": min_price}))
        if max_price:
            query['must'].append(Q("range", price={"lte": max_price}))
        if hotel_id:
            query['must'].append(Q("term", hotel=hotel_id))
        if is_available is not None:
            query['must'].append(Q("term", is_available=is_available.lower() == 'true'))

        search = search.query(query)[(page-1)*page_size:page*page_size]
        response = search.execute()

        rooms = [{
            'room_number': hit.room_number,
            'type': hit.type,
            'price': hit.price,
            'is_available': hit.is_available,
            'hotel_name': hit.hotel['name'],
        } for hit in response]

        result_page = pagination.paginate_queryset(rooms, request)
        serializer = RoomSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHE_TIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)