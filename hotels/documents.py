from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django.contrib.auth import get_user_model

from .models.hotel_models import Hotel
from hotels.models.city_models import City

User = get_user_model()

@registry.register_document
class HotelDocument(Document):
    city = fields.ObjectField(properties={
        'name': fields.TextField(),
    })
    class Index:
        name = 'hotels'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1
        }

    class Django:
        model = Hotel
        fields = [
            'name',
            'address',
            'star_rating',
            'status',
            'breakfast_price',
            'check_in_time',
            'check_out_time',
        ]
        related_models = [City]

    def get_instances_from_related(self, instance):
        if isinstance(instance, City):
            return instance.hotels.all()