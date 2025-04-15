from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics

from hotels.models.hotel_models import Hotel
from hotels.serializers.hotel_serializer import HotelSerializer
from utils.permissions import  HeHasPermission, IsOwnerOrReadOnly, IsEmailVerified

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
    
