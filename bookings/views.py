from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.db import transaction

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
        result_page = pagination.paginate_queryset(bookings, request)
        serializer = BookingSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)
    

class CreateBookingAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmailVerified]

    def post(self, request, room_id):
        with transaction.atomic():
            user = request.user  
            room = get_object_or_404(Room.objects.select_for_update(), id=room_id)
            serializer = BookingSerializer(data=request.data, many=False)
            if serializer.is_valid():
                check_in = serializer.validated_data['check_in_date']
                check_out = serializer.validated_data['check_out_date']
                conflicting_dates = Booking.objects.filter(
                    hotel=room.hotel,
                    room=room,
                    check_in_date__lte=check_out,
                    check_out_date__gte=check_in
                )
                if conflicting_dates:
                    return Response(
                        {'message': 'This room already reserved by somebody else'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                room.is_available = False
                room.save()
                serializer.save(user=user, room=room, hotel=room.hotel)
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
        room = booking.room
        with transaction.atomic():
            if request.user == booking.user:
                booking.delete()
                room.is_available = True
                room.save()
                return Response({'message': 'Booking deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)


from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta

from accounts.models import CustomUser
from hotels.models.hotel_models import Hotel
from rooms.models.room_models import Room
from bookings.models import Booking

from rest_framework_simplejwt.tokens import RefreshToken


class BookingViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="pass", is_verified=True)
        self.user2 = CustomUser.objects.create_user(username="otheruser", password="pass", is_verified=True)

        self.hotel = Hotel.objects.create(name="Test Hotel", breakfast_price=10.00)
        self.room = Room.objects.create(hotel=self.hotel, room_number="101", price=100.00, is_available=True)

        self.booking = Booking.objects.create(
            user=self.user,
            hotel=self.hotel,
            room=self.room,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=2),
            breakfast_order=False
        )

        self.client = APIClient()
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_user_bookings_list(self):
        url = reverse("user-bookings-list")  # You must define this name in your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_create_booking_success(self):
        url = reverse("create-booking", kwargs={"room_id": self.room.id})  # Define this name in urls
        data = {
            "check_in_date": str(date.today() + timedelta(days=5)),
            "check_out_date": str(date.today() + timedelta(days=7)),
            "breakfast_order": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["room"], self.room.id)

    def test_create_booking_conflict(self):
        url = reverse("create-booking", kwargs={"room_id": self.room.id})
        # Conflict with existing booking
        data = {
            "check_in_date": str(self.booking.check_in_date),
            "check_out_date": str(self.booking.check_out_date + timedelta(days=1)),
            "breakfast_order": False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "This room already reserved by somebody else")

    def test_get_booking_detail(self):
        url = reverse("booking-detail", kwargs={"booking_id": self.booking.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.booking.id)

    def test_patch_booking(self):
        url = reverse("booking-detail", kwargs={"booking_id": self.booking.id})
        response = self.client.patch(url, {"breakfast_order": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["breakfast_order"])

    def test_delete_booking(self):
        url = reverse("booking-detail", kwargs={"booking_id": self.booking.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_booking_by_other_user_forbidden(self):
        # Login as different user
        token = str(RefreshToken.for_user(self.user2).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse("booking-detail", kwargs={"booking_id": self.booking.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
