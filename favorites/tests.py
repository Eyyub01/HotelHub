from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from accounts.models import CustomUser
from hotels.models.hotel_models import Hotel
from rooms.models.room_models import Room
from hotels.models.city_models import City
from favorites.models import Favorite
from rest_framework_simplejwt.tokens import RefreshToken


class FavoriteViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass", email="test@example.com")
        self.user.is_verified = True
        self.user.save()

        self.city = City.objects.create(name="Test City")
        self.hotel = Hotel.objects.create(name="Test Hotel", city=self.city)
        self.room = Room.objects.create(hotel=self.hotel, room_number="101", price=100)

        self.client = APIClient()
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_favorite_for_hotel(self):
        url = reverse('create-favortie-hotel', kwargs={'hotel_id': self.hotel.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.count(), 1)
        self.assertEqual(Favorite.objects.first().hotel, self.hotel)

    def test_create_favorite_for_room(self):
        url = reverse('create-favortie-room', kwargs={'room_id': self.room.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.count(), 1)
        self.assertEqual(Favorite.objects.first().room, self.room)

    def test_list_favorites(self):
        Favorite.objects.create(user=self.user, room=self.room)
        url = reverse('favorite-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_favorite_detail(self):
        favorite = Favorite.objects.create(user=self.user, hotel=self.hotel)
        url = reverse('favorite-detail', kwargs={'favorite_id': favorite.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], favorite.id)

    def test_delete_favorite(self):
        favorite = Favorite.objects.create(user=self.user, hotel=self.hotel)
        url = reverse('favorite-detail', kwargs={'favorite_id': favorite.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Favorite.objects.count(), 0)
