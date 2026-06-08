from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('guest', 'guest'),
        ('admin', 'admin')
    )
    role = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='guest')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.role}'