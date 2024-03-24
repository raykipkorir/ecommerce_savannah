from rest_framework import serializers
from rest_framework.validators import ValidationError

from carts.models import CartItem
from products.serializers import ProductSerializer

from .models import Order, OrderItem
from .send_sms import send


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ("id", "status", "address", "phone_number", "total_amount", "product")


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "address", "phone_number")

    def create(self, validated_data):
        request = self.context["request"]
        cart_items = CartItem.objects.filter(cart__customer=request.user)
        if cart_items.count() == 0:
            raise ValidationError({"detail": "No product in cart"})
        total_amount = sum([cart_item.product.price * cart_item.quantity for cart_item in cart_items])
        order = Order.objects.create(
            status="Acknowledged",
            address=validated_data["address"],
            phone_number=validated_data["phone_number"],
            total_amount=total_amount,
            customer=request.user
        )
        OrderItem.objects.bulk_create(
            [
                OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity) for cart_item in cart_items
            ]
        )
        # decrement quantity in stock after order is made
        for cart_item in cart_items:
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()

        cart_items.delete()
        # handle payment

        # send sms via africa's talking
        send(request.user.get_full_name(), validated_data["phone_number"])

        return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "status")


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product")
