from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'room_type',
            'description',
            'price_per_night',
            'capacity',
            'image',
            'is_available',
            'amenities',
            'created_at'
        ]
