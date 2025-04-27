from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models.room_models import Room
from hotels.models.hotel_models import Hotel

@registry.register_document
class RoomDocument(Document):
    hotel = fields.ObjectField(properties={
        'name': fields.TextField(),
        'id': fields.IntegerField(),
        'city': fields.TextField(),  
        'star_rating': fields.IntegerField(),  
    })

    class Index:
        name = 'rooms'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1
        }

    class Django:
        model = Room
        fields = [
            'room_number',
            'type',
            'price',
            'is_available',
            'description',
        ]
        related_models = [Hotel]

    def get_instances_from_related(self, instance):
        if isinstance(instance, Hotel):
            return instance.rooms.all()

    def prepare_price(self, instance):
        return str(instance.price)  