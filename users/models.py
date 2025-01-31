from django.db import models
from django.contrib.auth.models import AbstractUser


# Definicja ról użytkowników
USER_ROLES = [
    ('admin', 'Administrator'),
    ('seller', 'Sprzedawca'),
    ('buyer', 'Kupujący'),
    ('vip_buyer', 'Kupujący VIP'),
]


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='buyer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    vip_bonus = models.BooleanField(default=False)  # Dodatkowe korzyści dla VIP-ów

    def save(self, *args, **kwargs):
        """Automatycznie przypisuje korzyści VIP-om"""
        if self.role == 'vip_buyer':
            self.vip_bonus = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"