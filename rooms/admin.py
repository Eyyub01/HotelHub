from django.contrib import admin
from rooms.models.room_models import Room


admin.site.site_header = "HotelHub Management"
admin.site.site_title = "HotelHub Admin Panel"
admin.site.index_title = "Welcome to HotelHub Administration"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ('room_number', 'type', 'hotel__name')  
    list_display = ('room_number', 'type', 'hotel', 'price', 'is_available')
    list_filter = ('type', 'is_available', 'hotel')
    autocomplete_fields = ('hotel',)  
