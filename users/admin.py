from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Dodatkowe informacje', {'fields': ('role', 'phone_number', 'address',
                                             'vip_bonus')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
