from pydantic import BaseModel

class SessionModel(BaseModel):
    pk: str  # 사용자 ID
    sk: str = "session"  # 세션 키
    access_token: str
    refresh_token: str
    expires_at: int  # UNIX timestamp
