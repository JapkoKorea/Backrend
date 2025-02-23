from dotenv import load_dotenv
import os
import httpx

load_dotenv()
KAKAO_TOKEN_URL = os.getenv('KAKAO_TOKEN_URL')
KAKAO_USER_INFO_URL = os.getenv('KAKAO_USER_INFO_URL')


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
        print('응답:', response)
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
