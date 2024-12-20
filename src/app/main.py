from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routers import records, healthcheck, click
import os
# FastAPI 앱 생성
app = FastAPI(
    title="MSA Example",
    description="Kafka와 DynamoDB를 활용한 기록 저장 서비스",
    version="1.0.0"
)

# CORS 설정 (필요시 수정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (CSS, JS 등)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)

# HTML 템플릿 서빙
@app.get("/")
async def root():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    print(type(html_content))
    return HTMLResponse(content=html_content, media_type="text/html")

# 라우터 등록
# app.include_router(records.router, prefix="/records", tags=["Records"])
# app.include_router(healthcheck.router, prefix="/health", tags=["Health Check"])
# app.include_router(click.router, prefix="/api", tags=["Click Logs"])
app.include_router(click.router, prefix="/click", tags=["Click Logs"])
app.include_router(healthcheck.router, prefix="/health", tags=["Health Check"])


# 앱 실행 (Docker Compose에서 uvicorn 실행 사용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
