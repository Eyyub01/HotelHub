from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from hotels.models.city_models import City
from hotels.models.hotel_models import Hotel
from rooms.models.room_models import Room

CustomUser = get_user_model()


class RoomAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='pass1234', is_email_verified=True)
        self.city = City.objects.create(name="Test City")
        self.hotel = Hotel.objects.create(name="Hotel One", owner=self.user, city=self.city)
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number='101',
            type='SGL',
            price=100.00,
            is_available=True
        )

    def test_list_rooms(self):
        response = self.client.get(reverse('room-list'))  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_list_rooms_cache(self):
        url = reverse('room-list') + "?page=1&page_size=10"
        self.client.get(url)  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_room_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'hotel': self.hotel.id,
            'room_number': '102',
            'type': 'DBL',
            'price': '150.00',
            'is_available': True
        }
        response = self.client.post(reverse('room-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_room_unauthenticated(self):
        data = {
            'hotel': self.hotel.id,
            'room_number': '103',
            'type': 'DBL',
            'price': '150.00',
            'is_available': True
        }
        response = self.client.post(reverse('room-create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_room_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('room-detail', kwargs={'room_id': self.room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['room_number'], '101')

    def test_update_room_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('room-detail', kwargs={'room_id': self.room.id})
        data = {
            'hotel': self.hotel.id,
            'room_number': '101',
            'type': 'DBL',
            'price': 120.00,
            'is_available': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], 'DBL')

    def test_delete_room_owner(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('room-detail', kwargs={'room_id': self.room.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
