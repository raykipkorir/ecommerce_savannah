from pathlib import Path

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carts.models import Cart, CartItem
from ecommerce.utils import authenticate_as_admin, authenticate_as_normal_user
from orders.models import Order, OrderItem
from products.models import Product


class TestOrderAPI(APITestCase):
    def setUp(self) -> None:
        self.test_image_path = (
            Path(__file__).resolve().parent.parent.parent / "static/test_image.jpg"
        )
        self.product = Product.objects.create(
            name="Laptop",
            description="Best laptop for software engineering",
            price=20000,
            stock=10
        )

    def create_order(self, user_type) -> Order:
        if user_type == "admin":
            user = authenticate_as_admin(self.client)
        else:
            user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        CartItem.objects.create(cart=cart, product=self.product)
        order = Order.objects.create(
            address="Nairobi",
            phone_number="254700000000",
            total_amount=20000,
            customer=user
        )
        return order

    def test_order_create_api(self) -> None:
        self.create_order("normal_user")
        response = self.client.post(
            reverse("orders-list"),
            data={"address": "Nairobi", "phone_number": "+254700000000"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_create_fail_when_unauthenticated(self) -> None:
        response = self.client.post(
            reverse("orders-list"),
            data={"address": "Nairobi", "phone_number": "+254700000000"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_create_fail_when_there_is_no_product_in_cart(self) -> None:
        authenticate_as_normal_user(self.client)
        response = self.client.post(
            reverse("orders-list"),
            data={"address": "Nairobi", "phone_number": "+254700000000"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_api(self) -> None:
        authenticate_as_normal_user(self.client)
        response = self.client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_update_api(self) -> None:
        order = self.create_order("admin")
        response = self.client.put(
            reverse("orders-detail", kwargs={"pk": order.pk}),
            data={"status": "Delivered"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_api(self) -> None:
        order = self.create_order("normal_user")
        response = self.client.get(reverse("orders-detail", kwargs={"pk": order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_when_authenticated_as_admin(self) -> None:
        order = self.create_order("admin")
        response = self.client.get(reverse("orders-detail", kwargs={"pk": order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_delete_api(self) -> None:
        order = self.create_order("admin")
        response = self.client.delete(reverse("orders-detail", kwargs={"pk": order.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_order_item_list_api(self) -> None:
        order = self.create_order("normal_user")
        response = self.client.get(reverse("order-items-list", kwargs={"orders_pk": order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_item_list_fail_when_unauthenticated(self) -> None:
        response = self.client.get(reverse("order-items-list", kwargs={"orders_pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_item_update_api(self) -> None:
        order = self.create_order("admin")
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2)
        response = self.client.put(
            reverse("order-items-detail", kwargs={"orders_pk": order.pk, "pk": order_item.pk}),
            data={"quantity": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_item_delete_api(self) -> None:
        order = self.create_order("admin")
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=2)
        response = self.client.delete(
            reverse("order-items-detail", kwargs={"orders_pk": order.pk, "pk": order_item.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
