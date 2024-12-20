from fastapi import APIRouter
from services.kafka_service import send_click_record

router = APIRouter()

@router.post("/")
async def create_record():
    """
    버튼 클릭 기록을 Kafka로 전송
    """
    try:
        send_click_record("User clicked the button")
        return {"message": "클릭 기록이 Kafka로 전송되었습니다."}
    except Exception as e:
        return {"error": str(e)}
