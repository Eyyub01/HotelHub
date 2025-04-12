# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Customer

# @admin.register(Customer)
# class CustomerAdmin(UserAdmin):
#     list_display = ['username', 'email', 'phone_number', 'created_at']
#     list_filter = ['is_staff', 'is_superuser', 'created_at']
#     search_fields = ['username', 'email', 'phone_number']
    
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'phone_number', 'profile_picture'),
#         }),
#     )
    
#     ordering = ['email']
#     readonly_fields = ['created_at', 'updated_at']