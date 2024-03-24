from rest_framework import serializers
from rest_framework.validators import ValidationError

from products.models import Product
from products.serializers import ProductSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(min_value=1, write_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ("id", "product", "product_id", "quantity")

    def create(self, validated_data):
        request = self.context["request"]
        try:
            product = Product.objects.get(id=validated_data.get("product_id"))
        except Product.DoesNotExist:
            raise ValidationError({"product_id": "Product not found"})

        cart = Cart.objects.get(customer=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).exists()
        if cart_item:
            raise ValidationError({"detail": "Product already in cart"})

        if validated_data.get("quantity"):
            if product.stock < validated_data.get("quantity"):
                raise ValidationError({"detail": "Product's stock is not enough"})
            quantity = validated_data.get("quantity")
        else:
            if product.stock < 1:
                raise ValidationError({"detail": "Product is out of stock"})
            quantity = 1

        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )
        return cart_item


class CartItemUpdateSerializer(serializers.ModelSerializer):
    action = serializers.CharField(required=True, write_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "action")

    def validate_action(self, value):
        if value.lower() not in ["increase", "decrease"]:
            raise ValidationError({"action": "increase or decrease are the only options"})
        return value

    def update(self, instance, validated_data):
        if validated_data.get("action").lower() == "increase":
            if instance.product.stock < 1:
                raise ValidationError({"detail": "Product is out of stock"})
            instance.quantity += 1
        else:
            if instance.quantity <= 1:
                raise ValidationError({"detail": "Quantity of product can't go below 1"})
            instance.quantity -= 1
        instance.save()
        return instance
