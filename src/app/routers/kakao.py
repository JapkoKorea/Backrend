from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from routers.kakao_handler import get_kakao_access_token, get_kakao_user_info
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import JSONResponse
from services.jwt_service import create_access_token, create_refresh_token
# from services.session_service import create_user_session, validate_user_session
import httpx
from services.dynamodb_service import delete_session
from services.dynamodb_service import save_user, get_user_by_pk
from models.user_model import UserModel
import uuid
from urllib.parse import quote
router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# 세션에 저장된 리프레시 토큰
active_refresh_tokens = {}

@router.get("/kakao_success")
async def success_page(request: Request):
    return templates.TemplateResponse("kakao_success.html", {"request": request})


KAKAO_CLIENT_ID = "46804a27702caeeef07d7f127980b015"
KAKAO_REDIRECT_URI = "http://localhost:8000/kakao/callback"


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
    print('카카오 액세스토큰:', kakao_access_token)
    print('유저 info:', user_info)
    # kakao_account = user_info.get("kakao_account", {})
    # birthday = kakao_account.get("birthday", "0000-00-00")
    # phone_number = kakao_account.get("phone_number", "000-0000-0000")
    
    # DynamoDB에서 사용자 정보 조회
    existing_user = get_user_by_pk(f"kakao#{kakao_id}")

    if not existing_user:
        # 신규 사용자 저장
        pk = str(uuid.uuid4())  # UUID로 사용자 고유 식별자 생성
        user = UserModel(
            pk=pk,
            sk="info",
            userName=user_name,
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


    # 로그인 상태를 DynamoDB에 저장 (또는 세션 유지)
    save_user(
        UserModel(
            pk=pk,
            sk="session",
            userName=user_name,
            birthday="", #birthday,
            phoneNumber="", #phone_number,
            OAuth=f"kakao#{kakao_id}",
        )
    )
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
    # access_token = request.cookies.get("access_token")  # 쿠키에서 토큰 가져오기
    # if not access_token:
    #     return RedirectResponse(url="/")
    # 카카오 로그아웃 요청
    kakao_logout_url = "https://kapi.kakao.com/v1/user/logout"
    headers = {"Authorization": f"Bearer {kakao_access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(kakao_logout_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to log out from Kakao")

    # 세션 정보 삭제
    user_info = await get_kakao_user_info(kakao_access_token)
    print("뽑은 유저 정보", user_info)
    # user_id = user_info['id']
    # if user_id:
    #     delete_session(user_id)

    # 쿠키 삭제 및 메인 페이지로 리디렉션
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    response.delete_cookie(key="user_name")
    response.delete_cookie(key="kakao_access_token")
    return response
    # """
    # 카카오 연결 끊기
    # """
    # user_info = await get_kakao_user_info(access_token)
    # if not user_info or "id" not in user_info:
    #     raise HTTPException(status_code=401, detail="Invalid access token or failed to fetch user info")

    # user_id = user_info["id"]

    # # 세션 삭제
    # # delete_session(user_id)
    # kakao_unlink_url = "https://kapi.kakao.com/v1/user/unlink"
    # headers = {"Authorization": f"Bearer {access_token}"}
    

    # async with httpx.AsyncClient() as client:
    #     response = await client.post(kakao_unlink_url, headers=headers)

    # if response.status_code == 200:
    #     return JSONResponse(content={"message": "Successfully logged out from Kakao"})
    # else:
    #     raise HTTPException(status_code=response.status_code, detail="Failed to log out from Kakao")