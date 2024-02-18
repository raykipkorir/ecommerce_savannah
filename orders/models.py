from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product

User = get_user_model()


class Order(models.Model):
    ORDER_STATUS = (
        ("Acknowledged", "Acknowledged"),
        ("Cancelled", "Cancelled"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUS)
    address = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    total_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through="orders.OrderItem")

    def __str__(self):
        return f"{self.customer.get_username()}'s order"


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.product} in {self.order.customer.get_username()}'s order"
