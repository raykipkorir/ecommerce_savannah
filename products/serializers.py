from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    description = serializers.CharField(min_length=20)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "updated_at",
            "created_at",
        )
