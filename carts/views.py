from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import CartItem
from .serializers import CartItemSerializer, CartItemUpdateSerializer


class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        serializer = CartItemSerializer(instance=cart_items, many=True)

        total_price = sum([cart_item.product.price * cart_item.quantity for cart_item in cart_items])
        return Response({"cart_items": serializer.data, "total_price": total_price})

    def get_queryset(self):
        cart_items = CartItem.objects.select_related("product").filter(
            cart__customer=self.request.user
        )
        return cart_items

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CartItemUpdateSerializer
        return CartItemSerializer
