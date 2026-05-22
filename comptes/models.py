from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Avocat', 'Avocat'),
        ('Secretaire', 'Secrétaire'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Avocat')

    def __str__(self):
        return f"{self.username} ({self.role})"