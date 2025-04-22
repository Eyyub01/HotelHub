from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from hotels.models.hotel_models import Hotel, Review
from hotels.serializers.hotel_serializer import HotelSerializer, ReviewSerializer
from utils.permissions import  HeHasPermission, IsOwnerOrReadOnly, IsEmailVerified

User = get_user_model()


@extend_schema(tags=["Hotels"])
class HotelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'star_rating'] 
    search_fields = ['name']

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]  
    

@extend_schema(tags=["Hotels"])
class HotelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsEmailVerified]
    authentication_classes = [JWTAuthentication]  
    

class WishlistView(APIView):

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({'detail': "Not allowed."}, status=403)
        user = get_object_or_404(User, id=user_id)
        hotels = user.wishlist.all()
        data = [{'id': hotel.id, 'name': hotel.name, 'location': hotel.location} for hotel in hotels]
        return Response(data)

    def post(self, request, user_id):
        if request.user.id != user_id:
            return Response({'detail': "Not allowed."}, status=403)
        hotel_id = request.data.get('hotel_id')
        hotel = get_object_or_404(Hotel, id=hotel_id)
        request.user.wishlist.add(hotel)
        return Response({'detail': 'Hotel added to wishlist'}, status=201)

    def delete(self, request, user_id, hotel_id):
        if request.user.id != user_id:
            return Response({'detail': "Not allowed."}, status=403)
        hotel = get_object_or_404(Hotel, id=hotel_id)
        request.user.wishlist.remove(hotel)
        return Response({'detail': 'Hotel removed from wishlist'}, status=204)


class HotelReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Review.objects.filter(hotel__id=hotel_id)

    def perform_create(self, serializer):
        hotel_id = self.kwargs['hotel_id']
        hotel = Hotel.objects.get(id=hotel_id)
        user = self.request.user

        # Prevent duplicate reviews
        if Review.objects.filter(hotel=hotel, user=user).exists():
            raise ValidationError("You have already reviewed this hotel.")

        serializer.save(hotel=hotel, user=user)