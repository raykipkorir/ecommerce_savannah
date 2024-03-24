from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (ConfirmEmailAPI, GithubCallback, GitHubLogin,
                    GoogleCallback, GoogleLogin)

urlpatterns = [
    path("google/", GoogleLogin.as_view(), name="google-login"),
    path("github/", GitHubLogin.as_view(), name="github-login"),
    path("google-callback/", GoogleCallback.as_view(), name="google-callback"),
    path("github-callback/", GithubCallback.as_view(), name="github-callback"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path("confirm-email/<key>/", ConfirmEmailAPI.as_view(), name="account_confirm_email"),
    path("verify-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
]
