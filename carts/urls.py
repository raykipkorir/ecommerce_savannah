from rest_framework_nested.routers import DefaultRouter

from .views import CartItemViewSet

router = DefaultRouter()
router.register("cart-items", CartItemViewSet, basename="cart-items")

urlpatterns = router.urls
