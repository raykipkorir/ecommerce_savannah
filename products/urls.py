from rest_framework_nested.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
urlpatterns = router.urls
