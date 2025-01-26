from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routers import click, kakao, auth
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(click.router, prefix="/click", tags=["Click Logs"])
app.include_router(kakao.router, prefix="/kakao", tags=["Kakao"])
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# index.html 렌더링
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 로그인 상태 확인 (쿠키 또는 세션 사용)
    is_logged_in = bool(request.cookies.get("access_token"))
    return templates.TemplateResponse(
        "index.html", {"request": request, "is_logged_in": is_logged_in}
    )
# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("templates/index.html", "r", encoding="utf-8") as file:
#         return file.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
