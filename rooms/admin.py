from django.contrib import admin
from rooms.models.room_models import Room
from rooms.models.room_photo_models import RoomPhoto


admin.site.site_header = "HotelHub Management"
admin.site.site_title = "HotelHub Admin Panel"
admin.site.index_title = "Welcome to HotelHub Administration"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ('room_number', 'type', 'hotel__name')
    list_display = ('room_number', 'type', 'hotel', 'price', 'is_available')
    list_filter = ('type', 'is_available', 'hotel')
    autocomplete_fields = ('hotel',)

    def get_search_results(self, request, queryset, search_term):
        # Autocomplete üçün axtarış nəticələrini fərdiləşdirin
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if 'hotel' in request.GET:
            queryset = queryset.filter(hotel__name__icontains=search_term)
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        # Decimal dəyərini sətirə çevirərək saxlayın
        obj.price = str(obj.price) if obj.price else None
        super().save_model(request, obj, form, change)


class RoomPhotoInline(admin.TabularInline):
    model = RoomPhoto
    extra = 1  # Boş şəkil formalarının sayı
    fields = ('image', 'uploaded_at')  # Göstəriləcək sahələr
    readonly_fields = ('uploaded_at',)  # Yalnız oxumaq üçün sahələr

@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ('room', 'image', 'uploaded_at')  # Siyahıda göstəriləcək sahələr
    list_filter = ('room', 'uploaded_at')  # Filtrlər
    search_fields = ('room__room_number', 'room__hotel__name')  # Axtarış sahələri
    readonly_fields = ('uploaded_at',)  # Yalnız oxumaq üçün sahələr