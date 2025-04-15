from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404

from rooms.models.room_models import Room
from utils.permissions import  HeHasPermission, IsOwnerOrReadOnly, IsEmailVerified
from utils.pagination import CustomPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

class RoomListView(APIView):
    """
    API view to list all rooms or create a new room.
    """
    permission_classes=[AllowAny]
    pagination_class = CustomPagination

    def get(self, request):
        pagination = self.pagination_class()
        rooms = Room.objects.all()
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
    