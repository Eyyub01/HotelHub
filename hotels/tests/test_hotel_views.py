from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from hotels.models.hotel_models import Hotel
from hotels.models.city_models import City

class HotelListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.city = City.objects.create(name="Test City", country="US")
        Hotel.objects.create(name="Hotel A", address="123 Street", city=self.city)
        Hotel.objects.create(name="Hotel B", address="456 Avenue", city=self.city)

    def test_get_all_hotels(self):
        response = self.client.get('/api/v1/hotels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "Hotel A")
        self.assertEqual(response.data['results'][1]['name'], "Hotel B")

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
        response = self.client.post('/api/v1/hotels/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Hotel C")

    def test_create_hotel_invalid(self):
        data = {"name": ""}
        response = self.client.post('/api/v1/hotels/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class HotelDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.city = City.objects.create(name="Test City", country="US")
        self.hotel = Hotel.objects.create(name="Hotel A", address="123 Street", city=self.city)

    def test_get_hotel_by_id(self):
        response = self.client.get(f'/api/v1/hotels/{self.hotel.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Hotel A")

    def test_update_hotel(self):
        data = {
            "name": "Updated Hotel A",
            "address": "123 Updated Street",
            "city": self.city.id,
            "star_rating": 4
        }
        response = self.client.put(f'/api/v1/hotels/{self.hotel.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Hotel A")

    def test_delete_hotel(self):
        response = self.client.delete(f'/api/v1/hotels/{self.hotel.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class HotelSearchAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.city = City.objects.create(name="Test City", country="US")
        Hotel.objects.create(name="Hotel A", address="123 Street", city=self.city)
        Hotel.objects.create(name="Hotel B", address="456 Avenue", city=self.city)

    def test_search_hotels(self):
        response = self.client.get('/api/v1/hotels/search/?query=Hotel A')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Hotel A")

    def test_search_no_results(self):
        response = self.client.get('/api/v1/hotels/search/?query=Nonexistent')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Message'], "There are no hotels")