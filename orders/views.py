from rest_framework.viewsets import ModelViewSet

from .models import Order, OrderItem
from .permissions import CustomOrderPermission, IsAdminOrOwner
from .serializers import CreateOrderSerializer, OrderSerializer, UpdateOrderSerializer, OrderItemSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = [CustomOrderPermission]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            orders = Order.objects.prefetch_related("customer", "product").all()
        else:
            orders = Order.objects.prefetch_related("customer", "product").filter(
                customer=self.request.user
            )
        return orders

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return UpdateOrderSerializer
        return OrderSerializer


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        order_items = OrderItem.objects.filter(order__pk=self.kwargs.get("orders_pk"))
        return order_items
