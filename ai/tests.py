from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache
from .models import AiResponse, CustomUser
from hotels.models.hotel_models import Hotel
from hotels.models.city_models import City
from rooms.models.room_models import Room
from .serializers import AiResponseSerializer

class AiSupportAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            role='Owner'
        )
        self.city = City.objects.create(name='Test City')
        self.hotel = Hotel.objects.create(
            owner=self.user,
            name='Test Hotel',
            address='123 Test St',
            city=self.city,
            phone='+1234567890',
            email='hotel@example.com',
            star_rating=3,
            status='approved'
        )
        self.room = Room.objects.create(
            hotel=self.hotel,
            room_number='101',
            type='SGL',
            price=100.00,
            is_available=True
        )
        self.client.force_authenticate(user=self.user)

    def test_ai_support_request_success(self):
        url = reverse('ai-support-request', args=[self.room.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Request is being processed')
        self.assertTrue(AiResponse.objects.filter(user=self.user, room_id=self.room.id).exists())

    def test_ai_support_response_cached(self):
        cache_key = f'AI_response_to_user_{self.user.id}_for_room_{self.room.id}'
        cached_data = {'response': 'cached reply'}
        cache.set(cache_key, cached_data, timeout=60)

        url = reverse('ai-support-response', args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, cached_data)

    def test_ai_support_response_from_db(self):
        ai_response = AiResponse.objects.create(
            user=self.user,
            room_id=self.room.id,
            ai_response='hello from db',
            processed=True
        )
        url = reverse('ai-support-response', args=[self.room.id])
        response = self.client.get(url)
        expected_data = AiResponseSerializer(ai_response).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_ai_support_response_not_found(self):
        url = reverse('ai-support-response', args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No AI response found', response.data['message'])