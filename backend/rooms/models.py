from django.db import models
from django.utils import timezone



ROOM_TYPE=[
    ('suite', 'suite'),
    ('apartment', 'apartment'),
    ('basic', 'basic')
]




class Room(models.Model):
    name=models.CharField(max_length=100, null=False, blank=False)
    room_type=models.CharField(choices=ROOM_TYPE, default='suite', null=False, blank=False)
    description=models.CharField(max_length=250, null=False, blank=False)
    price_per_night=models.DecimalField(max_digits=20, decimal_places=2)
    capacity=models.PositiveIntegerField(default=1)
    image=models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_available=models.BooleanField(default=False)
    amenities = models.JSONField(default=list, help_text='e.g., ["WiFi", "TV"]')
    created_at=models.DateTimeField(default=timezone.now)