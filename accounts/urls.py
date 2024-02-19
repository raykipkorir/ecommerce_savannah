from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path

from .views import ConfirmEmailAPI, GithubCallback, GitHubLogin, GoogleCallback, GoogleLogin

urlpatterns = [
    path("google/", GoogleLogin.as_view(), name="google-login"),
    path("github/", GitHubLogin.as_view(), name="github-login"),
    path("google-callback/", GoogleCallback.as_view(), name="google-callback"),
    path("github-callback/", GithubCallback.as_view(), name="github-callback"),

    path("confirm-email/<key>/", ConfirmEmailAPI.as_view(), name="account_confirm_email"),
    path("verify-email/", VerifyEmailView.as_view(), name="account_email_verification_sent")
]
