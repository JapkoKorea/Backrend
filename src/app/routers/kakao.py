from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from routers.kakao_handler import get_kakao_access_token, get_kakao_user_info
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import JSONResponse
from services.jwt_service import create_access_token, create_refresh_token
# from services.session_service import create_user_session, validate_user_session
import httpx
from services.dynamodb_service import delete_session
from services.dynamodb_service import save_user, get_user_by_pk, query_info
from models.user_model import UserModel
import uuid
from urllib.parse import quote
from utils import get_korea_time
router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# 세션에 저장된 리프레시 토큰
active_refresh_tokens = {}

@router.get("/kakao_success")
async def success_page(request: Request):
    return templates.TemplateResponse("kakao_success.html", {"request": request})


KAKAO_CLIENT_ID = "46804a27702caeeef07d7f127980b015"
KAKAO_REDIRECT_URI = "http://localhost:8000/kakao/callback"
KAKAO_LOGOUT_REDIRECT_URI = "http://localhost:8000/kakao/logout_success"

@router.get("/login")
async def kakao_login():
    # 카카오 로그인 URL 생성
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?response_type=code&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}"
    )
    return RedirectResponse(kakao_auth_url)


@router.get("/callback")
async def kakao_callback(code: str):
    print('yayaya',code)
    # Access Token 요청
    kakao_access_token = await get_kakao_access_token(code, KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI)
    if not kakao_access_token:
        raise HTTPException(status_code=400, detail="Failed to get Kakao access token")

    # 사용자 정보 가져오기
    user_info = await get_kakao_user_info(kakao_access_token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get Kakao user info")

    # 사용자 정보 추출
    kakao_id = user_info["id"]
    user_name = user_info["properties"].get("nickname", "Unknown")

    # kakao_account = user_info.get("kakao_account", {})
    # birthday = kakao_account.get("birthday", "0000-00-00")
    # phone_number = kakao_account.get("phone_number", "000-0000-0000")
    
    # DynamoDB에서 사용자 정보 조회
    existing_user = query_info(kakao_id)
    # existing_user = get_user_by_pk(f"kakao#{kakao_id}")

    if not existing_user:
        
        # 신규 사용자 저장
        pk = str(uuid.uuid4())  # UUID로 사용자 고유 식별자 생성
        user = UserModel(
            pk=pk,
            sk="info",
            userName=user_name,
            createdAt = get_korea_time(),
            birthday="", #birthday,
            phoneNumber="", #phone_number,
            OAuth=f"kakao#{kakao_id}"  # OAuth 속성 추가
        )
        save_user(user)
    else:
        
        # 기존 사용자 로드
        pk = existing_user["pk"]
    
    # JWT 토큰 생성
    jwt_access_token = create_access_token({"id": pk})
    refresh_token = create_refresh_token({"id": pk})


    # # 로그인 상태를 DynamoDB에 저장 (또는 세션 유지)
    # save_user(
    #     UserModel(
    #         pk=pk,
    #         sk="session",
    #         userName=user_name,
    #         birthday="", #birthday,
    #         phoneNumber="", #phone_number,
    #         OAuth=f"kakao#{kakao_id}",
    #     )
    # )
    # URL 인코딩으로 한글 문제 해결
    encoded_user_name = quote(user_name)
    # 메인 페이지로 리디렉션
    response = RedirectResponse(url="/")
    response.set_cookie(key="access_token", value=jwt_access_token, httponly=False)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=False)
    response.set_cookie(key="user_name", value=encoded_user_name, httponly=False) 
    response.set_cookie(key="kakao_access_token", value=kakao_access_token, httponly=False) 
    return response


@router.get("/logout")
async def kakao_logout(kakao_access_token: str):
    """카카오 로그아웃 처리"""
    # 카카오 로그아웃 요청
    kakao_logout_url = "https://kapi.kakao.com/v1/user/logout"
    headers = {"Authorization": f"Bearer {kakao_access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(kakao_logout_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to log out from Kakao")
    

    # 쿠키 삭제 및 메인 페이지로 리디렉션
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    response.delete_cookie(key="user_name")
    response.delete_cookie(key="kakao_access_token")
    return response


# @router.get("/logout")
# async def kakao_logout():
#     """
#     카카오 로그아웃 URL 생성 및 리디렉션
#     """
#     kakao_logout_url = (
#         f"https://kauth.kakao.com/oauth/logout"
#         f"?client_id={KAKAO_CLIENT_ID}"
#         f"&logout_redirect_uri={KAKAO_LOGOUT_REDIRECT_URI}"
#     )
#     return RedirectResponse(kakao_logout_url)

# @router.get("/logout_success")
# async def kakao_logout_success():
#     """
#     카카오 로그아웃 완료 후 처리
#     """
#     # 쿠키 삭제 (예: access_token, user_name 등)
#     response = RedirectResponse(url="/")
#     response.delete_cookie(key="access_token")
#     response.delete_cookie(key="refresh_token")
#     response.delete_cookie(key="kakao_access_token")
#     response.delete_cookie(key="user_name")
#     return response