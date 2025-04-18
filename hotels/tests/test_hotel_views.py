from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from hotels.models.hotel_models import Hotel
from hotels.models.city_models import City

class HotelCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.city = City.objects.create(name="Test City", country="US")

    def test_create_hotel(self):
        data = {
            "name": "Hotel C",
            "address": "789 Road",
            "city": self.city.id,
            "star_rating": 4
        }
        response = self.client.post('/api/v1/hotels/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Hotel C")

    def test_create_hotel_invalid(self):
        data = {"name": ""}
        response = self.client.post('/api/v1/hotels/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)