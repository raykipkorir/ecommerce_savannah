from pathlib import Path

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ecommerce.utils import authenticate_as_admin, authenticate_as_normal_user
from products.models import Product


class TestProductViewSet(APITestCase):
    """Product API tests"""

    def setUp(self) -> None:
        self.test_image_path = (
            Path(__file__).resolve().parent.parent.parent / "static/test_image.jpg"
        )
        self.valid_payload = {
            "name": "Product 1",
            "price": 1500,
            "stock": 100,
            "description": "This is the product description",
        }
        self.product = Product.objects.create(name="Product 2", price=1500, stock=200)

    def test_product_create_api(self) -> None:
        authenticate_as_admin(self.client)
        with open(self.test_image_path, "rb") as image_file:
            self.valid_payload["image"] = image_file
            response = self.client.post(
                reverse("products-list"), data=self.valid_payload
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            product = Product.objects.get(name="Product 1")
            self.assertEqual(product.name, self.valid_payload["name"])

    def test_product_create_fail_when_authenticated_as_normal_user(self) -> None:
        authenticate_as_normal_user(self.client)
        with open(self.test_image_path, "rb") as image_file:
            self.valid_payload["image"] = image_file
            response = self.client.post(
                reverse("products-list"), data=self.valid_payload
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_list_api(self) -> None:
        response = self.client.get(reverse("products-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_api(self) -> None:
        response = self.client.get(
            reverse("products-detail", kwargs={"pk": self.product.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_update_api(self) -> None:
        authenticate_as_admin(self.client)
        with open(self.test_image_path, "rb") as image_file:
            response = self.client.put(
                reverse("products-detail", kwargs={"pk": self.product.id}),
                data={
                    "name": "Product 3",
                    "price": 1000,
                    "stock": 200,
                    "description": "This is the product description",
                    "image": image_file,
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_delete_api(self) -> None:
        authenticate_as_admin(self.client)
        response = self.client.delete(reverse("products-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 204)
