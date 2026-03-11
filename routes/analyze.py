from fastapi import APIRouter, HTTPException
from models.schemas import EmailRequest, AnalysisResult
from services.analyzer import analyze_email
from services.gmail_service import get_recent_emails, get_or_create_label, move_to_phishing

# APIRouter : FastAPI에서 엔드포인트를 모아서 관리하는 도구
router = APIRouter(prefix="/analyze", tags=["분석"])


@router.post("", response_model=AnalysisResult)
def analyze(email: EmailRequest):
    """이메일 직접 입력 분석"""
    try:
        return analyze_email(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")


@router.post("/gmail", response_model=list[AnalysisResult])
def analyze_gmail(count: int = 5):
    """
    Gmail 받은편지함에서 최근 이메일을 가져와서 피싱 분석
    피싱으로 판단된 이메일은 자동으로 '📁 피싱의심' 폴더로 이동
    """
    try:
        emails, service = get_recent_emails(count)

        # 피싱의심 라벨 ID 가져오기 (없으면 자동 생성)
        label_id = get_or_create_label(service)

        results = []
        for email in emails:
            result = analyze_email(EmailRequest(
                sender=email["sender"],
                subject=email["subject"],
                body=email["body"]
            ))

            # 피싱으로 판단되면 자동으로 폴더 이동
            if result.is_phishing:
                move_to_phishing(service, email["id"], label_id)

            results.append(result)

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gmail 분석 중 오류 발생: {str(e)}")