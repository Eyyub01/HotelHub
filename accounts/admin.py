from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomerUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_email_verified', 'is_owner_requested', 'is_active', 'display_profile_picture')
    list_filter = ('role', 'is_email_verified', 'is_owner_requested', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    list_per_page = 25  

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('email', 'phone_number', 'profile_picture', 'role', 'is_owner_requested', 'is_email_verified', 'email_verification_code')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'role', 'password1', 'password2', 'is_owner_requested', 'is_email_verified'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'email_verification_code')

    def display_profile_picture(self, obj):
        """Profil şəklini admin panelində göstərir."""
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "No Image"
    display_profile_picture.short_description = 'Profile Picture'

    def get_queryset(self, request):
        """Optimallaşdırılmış queryset."""
        return super().get_queryset(request).select_related('groups')

admin.site.register(CustomUser, CustomerUserAdmin)