import os
import json
import anthropic
from dotenv import load_dotenv
from models.schemas import EmailRequest, AnalysisResult

load_dotenv()  # .env 파일에서 API 키 불러오기

SYSTEM_PROMPT = """
당신은 사이버 보안 전문가입니다. 이메일을 분석하고
반드시 아래 JSON 형식으로만 응답하세요.

{
  "is_phishing": true 또는 false,
  "risk_level": "LOW" 또는 "MEDIUM" 또는 "HIGH",
  "reason": "판단 근거 한 줄",
  "recommendation": "권고사항"
}

피싱 판단 기준:
- 긴급성 강조 (즉시, 24시간 내 등)
- 발신자 주소 위장
- 개인정보/금융정보 요구
- 의심스러운 링크
- 어색한 문법
"""

def analyze_email(email: EmailRequest) -> AnalysisResult:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"발신자: {email.sender}\n제목: {email.subject}\n본문: {email.body}"
        }]
    )

    raw = response.content[0].text.strip().strip("```json").strip("```")
    data = json.loads(raw)

    # 분석 결과에 발신자/제목 추가
    return AnalysisResult(
        sender=email.sender,
        subject=email.subject,
        **data
    )