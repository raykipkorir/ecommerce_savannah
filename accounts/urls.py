from django.urls import path

from .views import GithubCallback, GitHubLogin, GoogleCallback, GoogleLogin

urlpatterns = [
    path("google/", GoogleLogin.as_view(), name="google-login"),
    path("github/", GitHubLogin.as_view(), name="github-login"),
    path("google-callback/", GoogleCallback.as_view(), name="google-callback"),
    path("github-callback/", GithubCallback.as_view(), name="github-callback"),
]
