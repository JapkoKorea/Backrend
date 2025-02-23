from fastapi import APIRouter, HTTPException, Depends, Cookie
from pydantic import BaseModel
from datetime import datetime
import uuid
import json
import requests

# DB 관련 함수와 JWT 관련 함수
from services.dynamodb_service import save_reservation, query_info, query_info_pk
from services.jwt_service import verify_token
from services.dynamodb_service import get_user_by_pk
from routers.line import send_line_reservation
from utils.utils import get_korea_time

router = APIRouter()

class TaxiReservation(BaseModel):
    english_name: str
    contact_number: str
    tour_date: str  # 희망 투어 일자 (YYYY-MM-DD 형식)
    tour_start_time: str  # 희망 투어 출발 시각 (HH:MM 형식)
    tour_duration: str  # 희망하는 투어 시간
    number_of_people: int  # 투어 인원
    departure: str  # 출발지
    destination: str  # 도착지 (투어 후)
    desired_course: str  # 희망하는 코스

@router.post("/reserve")
async def reserve_taxi(reservation: TaxiReservation, user_id: str):
    # if not access_token:
    #     raise HTTPException(status_code=401, detail="Access token is missing")
    
    # # JWT 토큰을 통해 pk 추출
    # try:
    #     user_data = verify_token(access_token)
    #     # user_pk = user_data["id"]
    # except Exception as e:
    #     raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_data = user_id
    # DynamoDB에서 사용자 정보 조회
    existing_user = get_user_by_pk(user_data)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 해당 pk로 'info'를 조회해서 데이터가 존재하면 예약 데이터 저장
    existing_info = query_info_pk(user_data)
    if existing_info:  # 기존 사용자 정보가 있으면 예약 저장
        reservationNumber = str(uuid.uuid4())  # 예약 고유 ID 생성
        pk = "10e65f25-2fa0-49cb-a330-c82027962685" # Test용
        # pk = user_data  
        sk = f"reserve#{get_korea_time()}"  # sk: 'reserve#현재시간'

        reservation_data = {
            "pk": pk,
            "sk": sk,
            "englishName": reservation.english_name,
            "phoneNumber": reservation.contact_number,
            "tourDate": reservation.tour_date,
            "tourStartTime": reservation.tour_start_time,
            "tourDuration": reservation.tour_duration,
            "numberOfPeople": reservation.number_of_people,
            "departure": reservation.departure,
            "destination": reservation.destination,
            "tourCourse": reservation.desired_course,
            "reservationNumber": reservationNumber,
            "status": "pending",  # 예약 상태는 'pending'
            "createdAt": get_korea_time(),  # 예약 생성 시간
        }


        # 예약 데이터 저장
        save_reservation(reservation_data)
        send_line_reservation(reservation_data)
        # /line API 호출 (예약 후 필요한 외부 API 호출)
        # line_api_url = "https://api.line.com/v2/reservation"  # 예시 URL
        # headers = {
        #     "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # LINE API 인증 토큰
        #     "Content-Type": "application/json",
        # }
        # response = requests.post(line_api_url, data=json.dumps(reservation_data), headers=headers)
        
        # send_line_reservation(reservation_data)

        # if response.status_code != 200:
        #     raise HTTPException(status_code=response.status_code, detail="Failed to reserve via LINE API")
        
        # return {"message": "Reservation successful", "reservation_id": pk}
    else:
        raise HTTPException(status_code=400, detail="User information not available for reservation.")
