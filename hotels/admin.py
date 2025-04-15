from django.contrib import admin

from .models.hotel_models import Hotel
from .models.hotel_photo_models import HotelPhoto
from .models.city_models import City


class HotelPhotoInline(admin.TabularInline):
    model = HotelPhoto
    extra = 1  
    readonly_fields = ('uploaded_at',)

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_rating', 'created_at')
    list_filter = ('city', 'star_rating')
    search_fields = ('name', 'city',)
    inlines = [HotelPhotoInline]
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelPhoto)
admin.site.register(City)
