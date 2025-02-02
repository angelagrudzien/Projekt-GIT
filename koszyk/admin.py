from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total_price", "get_items_list")

    def get_items_list(self, obj):
        return obj.get_items_list()
    get_items_list.short_description = "Lista zakupów"

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)