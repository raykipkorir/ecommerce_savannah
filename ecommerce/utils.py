from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

def authenticate_as_admin(client) -> None:
    """Admin authentication"""
    user = User.objects.create_superuser(
        username="admin",
        email="admin@gmail.com",
        password="testing321"
    )

    access_token = AccessToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

def authenticate_as_normal_user(client) -> None:
    """Normal user authentication"""
    user = User.objects.create_user(
        username="normaluser",
        email="normaluser@gmail.com",
        password="testing321"
    )

    access_token = AccessToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
