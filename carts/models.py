from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()

class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through="carts.CartItem")

    def __str__(self):
        return f"{self.customer.username}'s cart"


class CartItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
