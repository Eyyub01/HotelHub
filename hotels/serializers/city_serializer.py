from rest_framework import serializers
from hotels.models.city_models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country']
from rest_framework import serializers
from hotels.models.city_models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country']