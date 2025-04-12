from django.test import TestCase
from hotels.models.city_models import City
from hotels.models.hotel_models import Hotel
from django.core.exceptions import ValidationError

class CityModelTest(TestCase):
    def test_create_city(self):
        city = City.objects.create(name="Baku", country="AZ")
        self.assertEqual(str(city), "Baku, AZ")
        self.assertEqual(city.name, "Baku")
        self.assertEqual(city.country.code, "AZ")

class HotelModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Baku", country="AZ")

    def test_create_hotel(self):
        hotel = Hotel.objects.create(
            name="Grand Plaza",
            address="123 Main Street",
            city=self.city,
            phone="+994123456789",
            email="info@grandplaza.com",
            description="A luxury hotel in Baku.",
            star_rating=5,
            check_in_time="14:00",
            check_out_time="11:00"
        )
        self.assertEqual(str(hotel), "Grand Plaza (Baku, AZ)")
        self.assertEqual(hotel.star_rating, 5)
        self.assertEqual(hotel.city, self.city)

    def test_invalid_phone_number(self):
        hotel = Hotel(
            name="Invalid Phone Hotel",
            address="456 Another Street",
            city=self.city,
            phone="12345",  # invalid format
            email="invalid@hotel.com",
            star_rating=3
        )
        with self.assertRaises(ValidationError):
            hotel.full_clean() 

    def test_default_times(self):
        hotel = Hotel.objects.create(
            name="Check Times Hotel",
            address="789 Some Street",
            city=self.city
        )
        self.assertEqual(str(hotel.check_in_time), "14:00")
        self.assertEqual(str(hotel.check_out_time), "11:00")


class CityModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Test City", country="US")

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Test City")
        self.assertEqual(self.city.country.code, "US")

    def test_city_string_representation(self):
        self.assertEqual(str(self.city), "Test City, US")
