import time
import uuid
from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from jose import JWTError, jwt
from services.db_service import save_record
from services.kafka_service import send_to_kafka
import hashlib

router = APIRouter()

# JWT Secret 및 알고리즘
JWT_SECRET = "your_jwt_secret_key"
JWT_ALGORITHM = "HS256"

class ClickLog(BaseModel):
    item_name: str
    page_url: str
    item_id: str

# def decode_jwt(token: str):
#     """
#     JWT 디코딩 및 검증
#     """
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         return payload
#     except JWTError as e:
#         raise HTTPException(status_code=401, detail=f"Invalid JWT Token: {str(e)}")

@router.post("/log_click")
async def log_click(request: Request, log: ClickLog):
    """
    클릭 로그를 DynamoDB에 저장 및 Kafka로 전송
    """
    user_id = None
    session_id = None

    # # JWT 토큰 확인
    # jwt_token = request.headers.get("Authorization")
    # if jwt_token and jwt_token.startswith("Bearer "):
    #     jwt_token = jwt_token.split(" ")[1]
    #     try:
    #         user_data = decode_jwt(jwt_token)
    #         user_id = user_data.get("user_id")  # JWT payload에서 user_id 가져오기
    #     except HTTPException:
    #         user_id = None

    # JWT 유효한 경우: 세션 ID 가져오기
    if user_id:
        session_id = request.cookies.get("session_id", str(uuid.uuid4()))
    else:
        # JWT 없는 경우: IP 주소 기반 user_id 생성
        client_host = request.client.host
        user_id = hashlib.md5(client_host.encode("utf-8")).hexdigest()
        session_id = request.cookies.get("session_id", str(uuid.uuid4()))

    # 클릭 로그 생성
    message = {
        "userId": user_id,
        "sessionId": session_id,
        "timestamp": int(time.time()),
        "pagename": log.pagename,
        "url": log.page_url,
        "movieId": log.item_id,
        "star": None,
    }
    print(message)
    # # Kafka로 메시지 전송
    # try:
    #     send_to_kafka("log_movie_click", message)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Failed to send log to Kafka: {str(e)}")

    # # DynamoDB에 로그 저장
    # try:
    #     save_record(f"user#{user_id}", f"click#{message['timestamp']}", message)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Failed to save log to DynamoDB: {str(e)}")

    # return {"status": "success", "message": "Log saved successfully"}
