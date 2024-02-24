from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "stock", "price"]
    search_fields = ["name"]


admin.site.register(Product, ProductAdmin)
