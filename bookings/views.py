from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import Booking
from .serializers import BookingSerializer
from rooms.models.room_models import Room

from utils.pagination import CustomPagination
from utils.permissions import IsEmailVerified, HeHasPermission


class UserBookingsListAPIView(APIView):
    """
    API view to retrieve bookings for the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    pagination_class = CustomPagination

    def get(self, request):
        pagination = self.pagination_class()
        bookings = Booking.objects.filter(user=request.user)
        result_page = pagination.paginate_queryset(bookings)
        serializer = BookingSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)
    

class CreateBookingAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmailVerified]

    def post(self, request, room_id):
        room = get_object_or_404(Room.objects.filter(is_available=True), id=room_id)
        serializer = BookingSerializer(data=request.data, many=False)
        if serializer.is_valid():
            room.is_available = False
            room.save()
            serializer.save(user=request.user, room=room, hotel=room.hotel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmailVerified, HeHasPermission]

    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def delete(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        if request.user == booking.user:
            booking.delete()
            return Response({'message': 'Booking deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)

