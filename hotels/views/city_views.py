from hotels.models.city_models import City
from hotels.serializers.city_serializer import CitySerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CityListView(APIView):
    @swagger_auto_schema(
        operation_summary="List all cities",
        responses={200: CitySerializer(many=True)},
    )
    def get(self, request):
        """
        Retrieve a list of all cities.
        """
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

class CityDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve a city by ID",
        responses={
            200: CitySerializer(),
            404: openapi.Response(description="City not found"),
        },
    )
    def get(self, request, pk):
        """
        Retrieve details of a specific city by its ID.
        """
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return Response({'Error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CitySerializer(city)
        return Response(serializer.data)
