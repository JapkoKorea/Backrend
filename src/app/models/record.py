from pydantic import BaseModel

class Record(BaseModel):
    id: str
    data: str


class KakaoUser(BaseModel):
    id: int
    nickname: str
    email: str = None
    profile_image: str = None