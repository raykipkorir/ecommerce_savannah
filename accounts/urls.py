from django.urls import path

from .views import GitHubLogin, GoogleLogin, github_callback, google_callback

urlpatterns = [
    path("google/", GoogleLogin.as_view(), name="google-login"),
    path("github/", GitHubLogin.as_view(), name="github-login"),
    path("google-callback/", google_callback, name="google-callback"),
    path("github-callback/", github_callback, name="github-callback"),
]
