from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from hotels.models.city_models import City

class CityListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        City.objects.create(name="City A", country="US")
        City.objects.create(name="City B", country="GB")

    def test_get_all_cities(self):
        response = self.client.get('/api/v1/cities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "City A")
        self.assertEqual(response.data[1]['name'], "City B")

class CityDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.city = City.objects.create(name="City A", country="US")

    def test_get_city_by_id(self):
        response = self.client.get(f'/api/v1/cities/{self.city.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "City A")
        self.assertEqual(response.data['country'], "US")

    def test_get_city_not_found(self):
        response = self.client.get('/api/v1/cities/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['Error'], "City not found")