# from fastapi import APIRouter, Depends, HTTPException, status, Request
# from fastapi.responses import JSONResponse
# from services.jwt_service import create_access_token, create_refresh_token, verify_token
# # from services.session_service import refresh_user_session


# router = APIRouter()

# # 임시 사용자 데이터베이스
# fake_users_db = {
#     "test_user": {"id": 1, "username": "test_user", "password": "test_password"}
# }

# # 세션에 저장된 리프레시 토큰
# active_refresh_tokens = {}

# @router.post("/login")
# async def login(username: str, password: str):
#     """사용자 로그인"""
#     user = fake_users_db.get(username)
#     if not user or user["password"] != password:
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     access_token = create_access_token({"sub": username})
#     refresh_token = create_refresh_token({"sub": username})
    
#     # 리프레시 토큰을 세션에 저장
#     active_refresh_tokens[refresh_token] = username

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer",
#     }

# @router.post("/logout")
# async def logout(refresh_token: str):
#     """사용자 로그아웃"""
#     if refresh_token in active_refresh_tokens:
#         del active_refresh_tokens[refresh_token]
#         return {"message": "Successfully logged out"}
#     raise HTTPException(status_code=400, detail="Invalid refresh token")

# @router.post("/refresh")
# async def refresh_token(user_id: str, refresh_token: str):
#     try:
#         verify_token(refresh_token)
#         new_access_token = create_access_token({"sub": user_id})
#         new_refresh_token = create_refresh_token({"sub": user_id})
#         # refresh_user_session(user_id, new_access_token, new_refresh_token)
#         return {"access_token": new_access_token, "refresh_token": new_refresh_token}
#     except ValueError as e:
#         raise HTTPException(status_code=401, detail=str(e))
    
# @router.get("/access-token")
# async def get_access_token(request: Request):
#     """
#     쿠키에서 Access Token 가져오기
#     """
#     access_token = request.cookies.get("access_token")
#     if not access_token:
#         raise HTTPException(status_code=401, detail="Access token not found")
#     return {"access_token": access_token}