from rest_framework.test import APITestCase

from ecommerce.utils import authenticate_as_normal_user
from orders.models import Order, OrderItem
from products.models import Product


class TestOrderModels(APITestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(
            name="Laptop",
            price=200000,
            stock=1,
            description="This is the description",
        )

    def test_order_model_instance_readable_string(self):
        user = authenticate_as_normal_user(self.client)
        order = Order.objects.create(
            customer=user,
            status="Acknowledged",
            address="Nairobi",
            total_amount=200000
        )
        self.assertEqual(f"{order.customer.get_username()}'s order", order.__str__())

    def test_order_item_model_instance_readable_string(self):
        user = authenticate_as_normal_user(self.client)
        order = Order.objects.create(
            customer=user,
            status="Acknowledged",
            address="Nairobi",
            total_amount=200000
        )
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2)
        self.assertEqual(f"{self.product} in {order_item.order.customer.get_username()}'s order", order_item.__str__())
