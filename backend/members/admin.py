from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number')
    list_filter = UserAdmin.list_filter + ('role',)
