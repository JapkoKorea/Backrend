from pydantic import BaseModel

class UserModel(BaseModel):
    pk: str  # 사용자 고유 ID (UUID)
    sk: str = "info"  # 항상 "info"로 설정
    userName: str  # 사용자 이름
    birthday: str  # 생년월일 (YYYY-MM-DD 형식)
    phoneNumber: str  # 휴대폰 번호
    OAuth: str
