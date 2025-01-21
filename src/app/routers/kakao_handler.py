# import os

# import requests

# from oauth.social_schema import SocialMember, PROVIDER_ENUM

# KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
# KAKAO_SECRET = os.getenv("KAKAO_SECRET")
# KAKAO_CALLBACK_URI = "http://127.0.0.1:5500/kakao/callback.html"

import httpx

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"


async def get_kakao_access_token(code: str, client_id: str, redirect_uri: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            KAKAO_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )
        if response.status_code != 200:
            return None
        return response.json().get("access_token")


async def get_kakao_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            KAKAO_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status_code != 200:
            return None
        return response.json()
