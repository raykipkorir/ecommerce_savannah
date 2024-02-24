from django.contrib import admin

from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "address", "phone_number", "status", "total_amount"]
    search_fields = ["customer__username"]
    list_filter = ["status"]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity"]
    search_fields = ["product"]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
