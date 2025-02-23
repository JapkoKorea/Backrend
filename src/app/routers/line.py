import os
import hmac
import hashlib
import base64
import requests
from fastapi import FastAPI, HTTPException, APIRouter, Header, Request
from pydantic import BaseModel
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_API_URL = os.getenv('LINE_API_URL')

# LINE Access Token 및 Channel Secret 설정
# LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET") 

# FastAPI의 APIRouter 인스턴스 생성
router = APIRouter()

# 메시지 요청 데이터 모델
class MessageRequest(BaseModel):
    user_id: str
    message: str

# LINE 메시지 보내기 함수
def send_line_reservation(text_dict: dict):
    specified_user_id = "Ubd8b9cb27f80c4ecca6ecc8c2565b23e"
    print('reservation 보내기 들어옴')

    text = f"""
    新規予約です！

    名前/name:  {text_dict['englishName']}
    日付/date: {text_dict['tourDate']}
    人数/number of person: {text_dict['numberOfPeople']}
    時間/time: {text_dict['tourStartTime']}
    出発地: {text_dict['departure']}
    到着地: {text_dict['destination']}
    利用時間: {text_dict['tourDuration']}
    番号/phone: {text_dict['phoneNumber']}
    コース(코스): 
    {text_dict['tourCourse']}
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    
    data = {
        "to": specified_user_id,
        "messages": [
            {"type": "text", "text": text}
        ]
    }

    response = requests.post(LINE_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# LINE 메시지 보내기 함수
def send_line_message(user_id: str, text: str):
    print('send_line_message 들어옴')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    print('상대방 유저id:', user_id)
    data = {
        "to": user_id,
        "messages": [
            {"type": "text", "text": text}
        ]
    }

    response = requests.post(LINE_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# 메시지를 특정 사용자에게 전송하는 엔드포인트
# @router.post("/send-message/")
# async def send_message(request: MessageRequest):
#     print('send_message 들어옴')
#     return send_line_message(request.user_id, request.message)

@router.post("/webhook")
async def webhook(request: dict):
#     request: Request,
#         x_line_signature: str = Header(None)  # 🔹 LINE에서 보낸 Signature 헤더 받기
# ):
#     body = await request.body()

#     # 🔹 LINE Signature 검증 (필수)
#     hash = hmac.new(
#         LINE_CHANNEL_SECRET.encode('utf-8'),
#         body,
#         hashlib.sha256
#     ).digest()
#     expected_signature = base64.b64encode(hash).decode('utf-8')

#     # Signature 검증 실패 시 401 Unauthorized 반환
#     if x_line_signature != expected_signature:
#         raise HTTPException(status_code=401, detail="Invalid signature")

#     # 요청 데이터 파싱
#     body_json = await request.json()
#     events = body_json.get("events", [])

#     for event in events:
#         if event["type"] == "message" and event["message"]["type"] == "text":
#             user_id = event["source"]["userId"]
#             received_text = event["message"]["text"]
#             send_line_message(user_id, f"당신이 보낸 메시지: {received_text}")

    events = request.get("events", [])
    # print('webhook 들어옴')

    for event in events:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_id = event["source"]["userId"]
            received_text = event["message"]["text"]

            # 받은 메시지를 그대로 응답
            send_line_message(user_id, f"당신이 보낸 메시지: {received_text}")

    return {"status": "ok"}

