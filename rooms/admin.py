# from django.contrib import admin
# from rooms.models.room_models import Room

# class RoomAdmin(admin.ModelAdmin):
#     list_display = ('room_number', 'get_type_display', 'hotel', 'price', 'is_available', 'created_at', 'updated_at')
#     list_filter = ('hotel', 'type', 'is_available')
#     search_fields = ('room_number', 'hotel__name')
#     ordering = ('hotel', 'room_number')
#     list_per_page = 20

#     fieldsets = (
#         (None, {
#             'fields': ('hotel', 'room_number', 'type', 'price', 'is_available')
#         }),
#         ('Optional Details', {
#             'fields': ('description',),
#             'classes': ('collapse',)
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

#     readonly_fields = ('created_at', 'updated_at')

# admin.site.register(Room, RoomAdmin)
from django.contrib import admin
from rooms.models.room_models import Room

admin.site.register(Room)

admin.site.site_header = "HotelHub Management"
admin.site.site_title = "HotelHub Admin Panel"
admin.site.index_title = "Welcome to HotelHub Administration"
