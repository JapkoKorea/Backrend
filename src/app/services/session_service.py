# from time import time
# from models.session_model import SessionModel
# # from services.dynamodb_service import save_session, get_session, delete_session
# SESSION_TIMEOUT_SECONDS = 1800  # 30분

# def create_user_session(pk: str, access_token: str, refresh_token: str):
#     expires_at = int(time() + SESSION_TIMEOUT_SECONDS)
#     session = SessionModel(pk=pk, access_token=access_token, refresh_token=refresh_token, expires_at=expires_at)
#     save_session(session)

# def validate_user_session(pk: str):
#     session = get_session(pk)
#     if not session or session["expires_at"] < time():
#         delete_session(pk)
#         raise ValueError("Session expired")
#     return session

# def refresh_user_session(pk: str, access_token: str, refresh_token: str):
#     delete_session(pk)
#     create_user_session(pk, access_token, refresh_token)


# # from datetime import datetime, timedelta
# # import hashlib

# # class SessionManager:
# #     def __init__(self):
# #         self.sessions = {}

# #     def get_session_id(self, user_id):
# #         now = datetime.now()
# #         if user_id not in self.sessions or self.sessions[user_id]['expires'] < now:
# #             # 새로운 세션 생성
# #             session_id = self._generate_session_id(user_id)
# #             self.sessions[user_id] = {
# #                 'session_id': session_id,
# #                 'expires': now + timedelta(minutes=30)
# #             }
# #         return self.sessions[user_id]['session_id']

# #     def _generate_session_id(self, user_id):
# #         # 고유한 세션 ID 생성 (예: 해시 사용)
# #         raw = f"{user_id}-{datetime.timestamp(datetime.now())}"
# #         return hashlib.sha256(raw.encode()).hexdigest()

# #     def extend_session(self, user_id):
# #         # 세션 갱신
# #         if user_id in self.sessions:
# #             self.sessions[user_id]['expires'] = datetime.now() + timedelta(minutes=30)

# # session_manager = SessionManager()
