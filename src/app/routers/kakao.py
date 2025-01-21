from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from routers.kakao_handler import get_kakao_access_token, get_kakao_user_info
from fastapi.templating import Jinja2Templates
from fastapi import Request
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")



# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     """
#     JWT 액세스 토큰 생성
#     """
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


@router.get("/success")
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


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
    access_token = await get_kakao_access_token(code, KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI)
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to get Kakao access token")

    # 사용자 정보 가져오기
    user_info = await get_kakao_user_info(access_token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get Kakao user info")

    # return {"message": "Kakao login successful", "user_info": user_info}
    # 처리 후 홈 페이지로 리디렉션
    return RedirectResponse(url="/kakao_success")  # 성공 페이지로 리디렉션 