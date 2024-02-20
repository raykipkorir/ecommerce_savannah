import requests
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class GoogleLogin(SocialLoginView):
    """Google login"""
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_CALLBACK_URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        return response


class GitHubLogin(SocialLoginView):
    """GitHub login"""
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.GITHUB_CALLBACK_URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        return response


class GoogleCallback(APIView):
    """Google callback"""
    def get(self, request, *args, **kwargs):
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
        )
        res = requests.post(
            request.build_absolute_uri(reverse("google-login")),
            data={"access_token": res.json()["access_token"]},
        )
        return Response(res.json())


class GithubCallback(APIView):
    """Github callback"""
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        res = requests.post(
            request.build_absolute_uri(reverse("github-login")),
            data={"code": code},
        )
        return Response(res.json())


class ConfirmEmailAPI(GenericAPIView):
    def get(self, request, *args, **kwargs):
        key = self.kwargs["key"]
        res = requests.post(
            request.build_absolute_uri(reverse("account_email_verification_sent")),
            data={"key": key}
        )
        return Response(res.json(), status=res.status_code)
