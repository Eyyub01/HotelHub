from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema

from rest_framework import filters, generics

from hotels.models.hotel_models import Hotel
from hotels.serializers.hotel_serializer import HotelSerializer


@extend_schema(tags=["Hotels"])
class HotelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'star_rating'] 
    search_fields = ['name']
    

@extend_schema(tags=["Hotels"])
class HotelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
