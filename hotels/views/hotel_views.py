from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http import Http404

from hotels.utils.pagination import CustomPagination
from hotels.serializers.hotel_serializer import HotelSerializer
from hotels.models.hotel_models import Hotel
from hotels.utils.permissions import IsOwnerOrReadOnly

class HotelListView(APIView):
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get(self, request):
        pagination = self.pagination_class()
        hotels = Hotel.objects.all()
        if hotels.exists():
            result_page = pagination.paginate_queryset(hotels, request)
            serializer = HotelSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There are no hotels'}, status=status.HTTP_400_BAD_REQUEST)

class HotelCreateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = HotelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HotelDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        hotel = self.get_object(pk)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    def put(self, request, pk):
        hotel = self.get_object(pk)
        data = request.data.copy()
        data['owner'] = hotel.owner.id
        serializer = HotelSerializer(hotel, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        hotel = self.get_object(pk)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HotelSearchAPIView(APIView):
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pagination = self.pagination_class()
        query = request.query_params.get('query', '')

        hotels = Hotel.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query) |
            Q(owner__username__icontains=query)
        ) if query else Hotel.objects.all()

        if hotels.exists():
            result_page = pagination.paginate_queryset(hotels, request)
            serializer = HotelSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)

        return Response({'Message': 'There are no hotels'}, status=status.HTTP_400_BAD_REQUEST)


class HotelFilterAPIView(APIView):
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Hotel.objects.all()

        name = request.query_params.get('name')
        city = request.query_params.get('city')
        country = request.query_params.get('country')
        star_rating = request.query_params.get('star_rating')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if country:
            queryset = queryset.filter(country__icontains=country)
        if star_rating:
            queryset = queryset.filter(star_rating=star_rating)

        if not queryset.exists():
            return Response({'message': 'No hotels found'}, status=status.HTTP_404_NOT_FOUND)

        pagination = self.pagination_class()
        result_page = pagination.paginate_queryset(queryset, request)
        serializer = HotelSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)
