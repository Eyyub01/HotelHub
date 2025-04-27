from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
import hashlib

from hotelhub.settings import CACHE_TIMEOUT
from hotels.documents import HotelDocument
from utils.pagination import CustomPagination
from hotels.models.hotel_models import Hotel, Review
from hotels.serializers.hotel_serializer import HotelSerializer, ReviewSerializer
from utils.permissions import  HeHasPermission, IsOwnerOrReadOnly, IsEmailVerified
from hotelhub.settings import CACHE_TIMEOUT


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

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)  
    

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
    


class HotelElasticSearchAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        pagination = self.pagination_class() 
        page = int(request.query_params.get('page', 1))
        page_size = self.pagination_class.page_size

        name = request.query_params.get('name', None)
        city = request.query_params.get('city', None)
        star_rating = request.query_params.get('star_rating', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)

        cache_key = hashlib.md5(
            f'hotel_search_name_{name}_city_{city}_star_rating_{star_rating}_'
            f'min_price_{min_price}_max_price_{max_price}_page_{page}_page_size_{page_size}'.encode()
        ).hexdigest()

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        search = Search(index="hotels")
        query = Q('bool', must=[])

        if name:
            query['must'].append(Q("match", name=name))
        if city:
            query['must'].append(Q("term", city=city))
        if star_rating:
            query['must'].append(Q("term", star_rating=star_rating))
        if min_price:
            query['must'].append(Q("range", price={"gte": min_price}))
        if max_price:
            query['must'].append(Q("range", price={"lte": max_price}))

        
        search = search.query(query)[(page-1)*page_size:page*page_size]
        response = search.execute()

        hotels = [{
            'name': hit.name,
            'address': hit.address,
            'star_rating': hit.star_rating,
            'status': hit.status,
            'city': hit.city['name'],
            'price': hit.price,
        } for hit in response]

    
        result_page = pagination.paginate_queryset(hotels, request)
        serializer = HotelSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        cache.set(cache_key, paginated_response, timeout=CACHE_TIMEOUT)
        return Response(paginated_response, status=status.HTTP_200_OK)