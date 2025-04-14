from django.db import models
from django_countries.fields import CountryField

class City(models.Model):
    name = models.CharField(
        max_length=100,
    )
    country = CountryField()

    def __str__(self):
        return f'{self.name}, {self.country}'
