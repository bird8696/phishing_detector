from pydantic import BaseModel
from typing import Optional


class EmailRequest(BaseModel):
    sender: Optional[str] = ""    # 발신자 (선택)
    subject: Optional[str] = ""   # 제목 (선택)
    body: str                      # 본문 (필수)


class AnalysisResult(BaseModel):
    # 이메일 정보
    sender: Optional[str] = ""    # 발신자
    subject: Optional[str] = ""   # 제목
    # 분석 결과
    is_phishing: bool              # 피싱 여부
    risk_level: str                # LOW / MEDIUM / HIGH
    reason: str                    # 판단 근거
    recommendation: str            # 권고사항