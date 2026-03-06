from fastapi import APIRouter, HTTPException
from models.schemas import EmailRequest, AnalysisResult
from services.analyzer import analyze_email

# APIRouter : FastAPI에서 엔드포인트를 모아서 관리하는 도구
router = APIRouter(prefix="/analyze", tags=["분석"])
# prefix="/analyze" → 이 라우터의 모든 주소 앞에 /analyze 가 붙어
# tags=["분석"] → Swagger UI에서 그룹으로 묶어서 보여줌

# 요청을 받는 엔드포인트
# response_model=AnalysisResult → 응답이 반드시 이 형태여야 함
# email: EmailRequest → 요청 본문을 자동으로 EmailRequest로 변환
@router.post("", response_model=AnalysisResult)
def analyze(email: EmailRequest):
    # Claude API 호출 중 오류가 나도 서버가 안 죽고 에러 메시지를 돌려줘
    try:
        return analyze_email(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")