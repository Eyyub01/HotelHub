from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'room', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'hotel__name', 'room__room_number')
