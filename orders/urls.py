from rest_framework_nested import routers

from .views import OrderItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")

orders_router = routers.NestedDefaultRouter(router, "orders", lookup="orders")
orders_router.register("items", OrderItemViewSet, basename="order-items")

urlpatterns = router.urls + orders_router.urls
