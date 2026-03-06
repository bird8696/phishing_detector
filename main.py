from fastapi import FastAPI
from dotenv import load_dotenv
from routes.analyze import router

load_dotenv()

# FastAPI 앱 생성하는 거야! `title`, `description`, `version` 은 `/docs` 에서 Swagger UI에 표시돼
app = FastAPI(
    title="피싱 이메일 탐지기",
    description="Claude AI를 활용한 피싱 이메일 분석 API",
    version="1.0.0"
)

# routes/analyze.py` 에서 만든 라우터를 앱에 등록하는 거야!
app.include_router(router)

# 서버 켰을 때 http://localhost:8000 접속하면 나오는 기본 응답
@app.get("/")
def root():
    return {"message": "피싱 탐지 서버 실행 중 🔐"}

if __name__ == "__main__":
    import uvicorn
    # python main.py` 로 직접 실행할 때 서버 켜주는 거야! 
    # `reload=True` 는 코드 수정하면 자동으로 서버 재시작해줘!
    uvicorn.run("main:app", reload=True)
    
    # 앱 생성 → 라우터 등록 → 서버 실행