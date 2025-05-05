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
        self.user = CustomUser.objects.create_user(username="testuser", password="pass", email="testuser@example.com",)
        self.user.is_verified = True 
        self.user2 = CustomUser.objects.create_user(username="otheruser", password="pass", email="testuser2@example.com",)
        self.user2.is_verified = True 
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
        url = reverse("user-bookings")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_create_booking_success(self):
        url = reverse("create-booking", kwargs={"room_id": self.room.id})
        self.room.is_available = True
        self.room.save()
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
        data = {
            "check_in_date": str(self.booking.check_in_date),
            "check_out_date": str(self.booking.check_out_date + timedelta(days=1)),
            "breakfast_order": False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "This room already reserved by somebody else")

    def test_get_booking_detail(self):
        url = reverse("booking-detail", kwargs={"room_id": self.booking.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.booking.id)

    def test_patch_booking(self):
        url = reverse("booking-detail", kwargs={"room_id": self.booking.id})
        response = self.client.patch(url, {"breakfast_order": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["breakfast_order"])

    def test_delete_booking(self):
        url = reverse("booking-detail", kwargs={"room_id": self.booking.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_booking_by_other_user_forbidden(self):
        token = str(RefreshToken.for_user(self.user2).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse("booking-detail", kwargs={"room_id": self.booking.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
