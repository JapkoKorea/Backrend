from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routers import click, kakao, auth, line, kakao_chat, reserve_taxi
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 생성
app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Next.js 개발 서버
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# templates = Jinja2Templates(directory="templates")
# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(click.router, prefix="/click", tags=["Click Logs"])
app.include_router(kakao.router, prefix="/kakao", tags=["Kakao"])
app.include_router(line.router, prefix="/line", tags=["Line"])
app.include_router(kakao_chat.router, prefix="/kakao_chat", tags=["Kakao Chatbot"])
app.include_router(reserve_taxi.router, prefix="/reserve_taxi", tags=["Reserve Taxi"])
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# index.html 렌더링
@app.get("/")
async def read_root():
    # # 로그인 상태 확인 (쿠키 또는 세션 사용)
    # is_logged_in = bool(request.cookies.get("access_token"))
    # return templates.TemplateResponse(
    #     "index.html", {"request": request, "is_logged_in": is_logged_in}
    # )
  return 'hello, server'
# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("templates/index.html", "r", encoding="utf-8") as file:
#         return file.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
