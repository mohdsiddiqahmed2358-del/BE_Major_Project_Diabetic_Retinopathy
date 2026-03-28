from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'department', 'date_joined']
    list_filter = ['role', 'date_joined', 'department']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role & Dates', {'fields': ('role', 'last_login', 'date_joined')}),
    )
    readonly_fields = ['date_joined', 'last_login']
