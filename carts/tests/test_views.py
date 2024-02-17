from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carts.models import Cart, CartItem
from ecommerce.utils import authenticate_as_normal_user
from products.models import Product


class TestCartItemAPI(APITestCase):
    """CartItem API tests"""
    def setUp(self) -> None:
        self.product = Product.objects.create(
            name="Laptop",
            price=200000,
            stock=1,
            description="This is the description",
        )

    def test_cart_item_create_success(self) -> None:
        user = authenticate_as_normal_user(self.client)
        Cart.objects.create(customer=user)
        response = self.client.post(
            reverse("cart-items-list"), data={"product_id": self.product.pk, "quantity": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_item = CartItem.objects.get(product__id=self.product.pk)
        self.assertEqual(cart_item.product.name, self.product.name)
        self.assertEqual(cart_item.quantity, 5)

    def test_cart_item_create_fail_when_product_is_not_available(self) -> None:
        authenticate_as_normal_user(self.client)
        response = self.client.post(
            reverse("cart-items-list"), data={"product_id": 10}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_item_create_fail_when_product_is_already_in_cart(self) -> None:
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        CartItem.objects.create(product=self.product, cart=cart)
        response = self.client.post(
            reverse("cart-items-list"), data={"product_id": self.product.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_item_list_api(self) -> None:
        authenticate_as_normal_user(self.client)
        response = self.client.get(reverse("cart-items-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_item_detail_api(self) -> None:
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart)
        response = self.client.get(
            reverse("cart-items-detail", kwargs={"pk": cart_item.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_item_increment_quantity_success(self) -> None:
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart)
        response = self.client.put(
            reverse("cart-items-detail", kwargs={"pk": cart_item.pk}),
            data={"action": "increase"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_item_increment_quantity_fail_when_product_out_of_stock(self) -> None:
        user = authenticate_as_normal_user(self.client)
        self.product.stock = 0
        self.product.save()
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart)
        response = self.client.put(
            reverse("cart-items-detail", kwargs={"pk": cart_item.pk}),
            data={"action": "increase"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_item_decrement_quantity_success(self) -> None:
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart, quantity=2)
        response = self.client.put(
            reverse("cart-items-detail", kwargs={"pk": cart_item.pk}),
            data={"action": "decrease"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_item_decrement_quantity_fail_when_quantity_of_cartitem_is_one(self) -> None:
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart, quantity=1)
        response = self.client.put(
            reverse("cart-items-detail", kwargs={"pk": cart_item.pk}),
            data={"action": "decrease"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_item_update_quantity_fail_when_passed_invalid_payload(self) -> None:
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart, quantity=2)
        response = self.client.put(
            reverse("cart-items-detail", kwargs={"pk": cart_item.pk}),
            data={"action": "decrement"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cart_item_delete_api(self) -> None:
        user = authenticate_as_normal_user(self.client)
        cart = Cart.objects.create(customer=user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart)
        response = self.client.delete(
            reverse("cart-items-detail", kwargs={"pk": cart_item.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
