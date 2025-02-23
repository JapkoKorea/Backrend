from fastapi import APIRouter

router = APIRouter()

# 예시 위치 데이터
locations = [
    {"lat": 37.5665, "lng": 126.9780, "title": "서울 시청"},
    {"lat": 37.5700, "lng": 126.9768, "title": "경복궁"},
    {"lat": 37.5759, "lng": 126.9764, "title": "광화문"},
    {"lat": 37.5566, "lng": 126.9435, "title": "홍대입구역"},
    {"lat": 37.5080, "lng": 127.0628, "title": "코엑스"},
    {"lat": 37.5512, "lng": 126.9882, "title": "남산타워"},
    {"lat": 37.5796, "lng": 126.9770, "title": "청와대"},
]

@router.get("/locations")
async def get_locations():
    return locations