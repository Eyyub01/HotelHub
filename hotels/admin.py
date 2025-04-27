from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.html import format_html

from .models.hotel_models import Hotel
from .models.hotel_photo_models import HotelPhoto
from .models.city_models import City


class HotelPhotoInline(admin.TabularInline):
    model = HotelPhoto
    extra = 1  
    readonly_fields = ('uploaded_at',)


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_rating', 'status', 'created_at')
    readonly_fields = ('status_actions',)
    list_filter = ('status', 'city', 'star_rating')
    search_fields = ('name', 'address', 'phone', 'email')

    def get_form(self, request, obj=None, **kwargs):
        # Store the request object
        self.request = request
        return super().get_form(request, obj, **kwargs)

    def status_actions(self, obj):
        from django.middleware.csrf import get_token
        
        if obj.status == 'approved':
            return "✅ Already Approved"
        elif obj.status == 'rejected':
            return "❌ Rejected"
        else:
            csrf_token = get_token(self.request)
            return format_html(
                '<form method="post" style="display:inline;">'
                '  <input type="hidden" name="csrfmiddlewaretoken" value="{}" />'
                '  <input type="hidden" name="approve" value="1" />'
                '  <button type="submit" class="button default">✅ Approve Hotel</button>'
                '</form>'
                '&nbsp;'
                '<form method="post" style="display:inline; margin-left: 8px;">'
                '  <input type="hidden" name="csrfmiddlewaretoken" value="{}" />'
                '  <input type="hidden" name="reject" value="1" />'
                '  <button type="submit" class="button deletelink" style="background-image: none;">❌ Reject Hotel</button>'
                '</form>',
                csrf_token, csrf_token
            )
    status_actions.short_description = "Hotel Moderation"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        hotel = Hotel.objects.get(pk=object_id)

        if request.method == "POST":
            if "approve" in request.POST and hotel.status != 'approved':
                hotel.status = 'approved'
                hotel.save()
                self.message_user(
                    request, f'✅ Hotel "{hotel.name}" approved successfully!',
                    messages.SUCCESS
                )
                return redirect(request.path)

            if "reject" in request.POST and hotel.status != 'rejected':
                hotel.status = 'rejected'
                hotel.save()
                self.message_user(
                    request, f'❌ Hotel "{hotel.name}" rejected successfully!',
                    messages.WARNING
                )
                return redirect(request.path)

        return super().change_view(request, object_id, form_url, extra_context)
    
   

admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelPhoto)
admin.site.register(City)
