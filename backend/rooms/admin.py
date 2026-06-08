from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price_per_night', 'capacity', 'is_available')
    list_filter = ('room_type', 'is_available', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Room Info', {'fields': ('name', 'room_type', 'description', 'image')}),
        ('Details', {'fields': ('price_per_night', 'capacity', 'amenities', 'is_available')}),
        ('Metadata', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)

