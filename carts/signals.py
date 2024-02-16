from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Cart


@receiver(user_logged_in)
def create_cart(request, user, **kwargs):
    """Create cart when user logs in via social provider"""
    # print(request, **kwargs)
    if not Cart.objects.filter(customer=user).exists():
        Cart.objects.create(customer=user)
