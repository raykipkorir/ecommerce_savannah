import requests
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_CALLBACK_URL
    client_class = OAuth2Client


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.GITHUB_CALLBACK_URL
    client_class = OAuth2Client


@api_view(["GET"])
def google_callback(request):
    code = request.GET.get("code")
    res = requests.post(
        "https://accounts.google.com/o/oauth2/token",
        params={
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": request.build_absolute_uri(reverse("google-callback")),
            "grant_type": "authorization_code",
            "code": code,
        },
        timeout=30
    )
    res = requests.post(
        request.build_absolute_uri(reverse("google-login")),
        data={"access_token": res.json()["access_token"]},
        timeout=30,
    )
    return Response(res.json())


@api_view(["GET"])
def github_callback(request):
    code = request.GET.get("code")
    res = requests.post(
        request.build_absolute_uri(reverse("github-login")),
        data={"code": code},
        timeout=30,
    )
    return Response(res.json())
