from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.http import Http404

from hotels.utils.pagination import CustomPagination
from hotels.serializers.hotel_serializer import HotelSerializer
from hotels.models.hotel_models import Hotel


class HotelListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        pagination = self.pagination_class()
        hotels = Hotel.objects.all()
        if hotels.exists():
            result_page = pagination.paginate_queryset(hotels, request)  
            serializer = HotelSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'Message': 'There are no hotels'}, status=status.HTTP_400_BAD_REQUEST)


class HotelCreateView(APIView):
    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelDetailView(APIView):
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
        serializer = HotelSerializer(hotel, data=request.data)
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

    def get(self, request, *args, **kwargs):
        pagination = self.pagination_class()
        query = request.query_params.get('query', '')
        hotels = Hotel.objects.filter(name__icontains=query) if query else Hotel.objects.all()
        
        if hotels.exists():
            result_page = pagination.paginate_queryset(hotels, request)
            serializer = HotelSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data) 
        return Response({'Message': 'There are no hotels'}, status=status.HTTP_400_BAD_REQUEST)
    

