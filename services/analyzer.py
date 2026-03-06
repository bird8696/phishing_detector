import os # 환경 변수 읽기용
import json # Claude 응답을 JSON으로 파싱
import anthropic # Claude API 연결
from dotenv import load_dotenv # .env 파일 읽기
from models.schemas import EmailRequest, AnalysisResult # models/schemass.py 내 데이터 구조

load_dotenv()  # .env 파일에서 API 키 불러오기(환경 변수 등록)

# Claude한테 "너는 보안 전문가야, JSON으로만 대답해" 라고 역할 부여
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
    # 1. Claude 클라이언트 생성 (API 키로 인증)
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # 2. Claude한테 이메일 분석 요청
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"발신자: {email.sender}\n제목: {email.subject}\n본문: {email.body}"
        }]
    )
    
    # 3. 응답에서 텍스트 꺼내기
    raw = response.content[0].text.strip().strip("```json").strip("```")
    
    # 4. JSON으로 파싱해서 AnalysisResult로 변환
    data = json.loads(raw)
    return AnalysisResult(**data)