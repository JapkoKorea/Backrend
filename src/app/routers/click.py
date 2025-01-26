import time
import uuid
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import hashlib
from services.jwt_service import verify_token


router = APIRouter()

class ClickData(BaseModel):
    image_id: str
    image_name: str
    timestamp: int

# 세션 관리 함수
session_cache = {}  # {user_id: {"session_id": str, "expires": datetime}}


@router.post("/")
async def log_click(request: Request, data: ClickData):
    # 사용자 정보 확인
    # client_host = request.client.host
    # user_id = hashlib.md5(client_host.encode("utf-8")).hexdigest()
    # 요청 헤더에서 Access Token 추출
    access_token = request.headers.get("Authorization")
    user_id = None
    if access_token:
        access_token = access_token.replace("Bearer ", "")
        payload = verify_token(access_token)
        user_id = payload['id']
    session_id = str(uuid.uuid4())

    # 로그 출력 -> 추후에 DB 저장 예정 
    print({
        "user_id": user_id,
        "session_id": session_id,
        "image_id": data.image_id,
        "image_name": data.image_name,
        "timestamp": data.timestamp,
    })

    return {"status": "success", "message": "Click logged successfully"}
