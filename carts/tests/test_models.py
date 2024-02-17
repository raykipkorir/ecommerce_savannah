from rest_framework.test import APITestCase
from carts.models import Cart, CartItem
from products.models import Product

from ecommerce.utils import authenticate_as_normal_user

class TestCartModels(APITestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(
            name="Laptop",
            price=200000,
            stock=1,
            description="This is the description",
        )
    def test_cart_model_instance_readable_string(self):
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        self.assertEqual(f"{cart.customer.username}'s cart", cart.__str__())

    def test_cart_item_model_instance_readable_string(self):
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product)
        self.assertEqual(f"{self.product.name} in {cart.customer.username}'s cart", cart_item.__str__())
