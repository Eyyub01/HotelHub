from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'hotel',
        'room',
        'check_in_date',
        'check_out_date',
        'total_price',
        'created_at',
        'updated_at',
    )
    list_filter = ('hotel', 'room', 'check_in_date', 'check_out_date')
    search_fields = ('user__username', 'hotel__name', 'room__room_number')  
    ordering = ('-created_at',)
    date_hierarchy = 'check_in_date'
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    autocomplete_fields = ('user', 'hotel', 'room')