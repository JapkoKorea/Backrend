from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routers import click, kakao

app = FastAPI()

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(click.router, prefix="/click", tags=["Click Logs"])
app.include_router(kakao.router, prefix="/kakao", tags=["Kakao"])

# index.html 렌더링
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return file.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
