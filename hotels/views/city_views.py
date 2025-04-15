from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from hotels.models.city_models import City
from hotels.serializers.city_serializer import CitySerializer


@extend_schema(tags=["Cities"])
class CityListView(APIView):
    def get(self, request):
        """
        Retrieve a list of all cities.
        """
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Cities"])
class CityDetailView(APIView):
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


