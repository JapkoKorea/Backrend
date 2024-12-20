from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def healthcheck():
    """
    서비스 헬스 체크
    """
    return {"status": "Healthy"}
