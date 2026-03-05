# 🔐 피싱 이메일 탐지기

Claude AI를 활용해 이메일의 피싱 여부를 자동으로 분석하는 FastAPI 기반 REST API 서버입니다.

---

## 📌 프로젝트 소개

피싱 이메일은 개인정보 탈취, 금융 사기 등에 악용되는 대표적인 사이버 공격입니다.  
이 프로젝트는 Anthropic의 **Claude AI**에게 보안 분석가 역할을 부여하여,  
별도의 학습 데이터 없이도 이메일의 피싱 여부를 높은 정확도로 판단합니다.

---

## 🗂 프로젝트 구조

```
phishing_detector/
├── main.py                # FastAPI 앱 진입점 및 서버 설정
├── requirements.txt       # 의존 패키지 목록
├── .env.example           # 환경변수 설정 템플릿
│
├── models/
│   └── schemas.py         # 요청/응답 데이터 구조 (Pydantic)
│
├── routes/
│   └── analyze.py         # API 엔드포인트 정의
│
└── services/
    └── analyzer.py        # Claude API 호출 및 분석 로직
```

---

## ⚙️ 설치 및 실행

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 환경변수 설정
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY에 실제 키 입력

# 3. 서버 실행
python main.py
# 또는
uvicorn main:app --reload
```

서버 실행 후 http://localhost:8000/docs 에서 Swagger UI로 바로 테스트 가능합니다.

---

## 🌐 API 명세

| 메서드 | 경로       | 설명             |
| ------ | ---------- | ---------------- |
| `GET`  | `/`        | 서버 상태 확인   |
| `POST` | `/analyze` | 이메일 피싱 분석 |

### 요청 예시

```json
POST /analyze
{
  "sender": "security@kak4o-bank.com",
  "subject": "[긴급] 계정이 잠겼습니다",
  "body": "24시간 내 아래 링크를 클릭하여 본인 인증을 완료해 주세요..."
}
```

### 응답 예시

```json
{
  "is_phishing": true,
  "risk_level": "HIGH",
  "reason": "발신자 도메인 위장 및 긴급성 유도 표현 사용",
  "recommendation": "링크를 클릭하지 말고 즉시 삭제하세요."
}
```

---

## 🛠 기술 스택

| 역할          | 기술                   |
| ------------- | ---------------------- |
| API 서버      | FastAPI                |
| AI 분석       | Claude API (Anthropic) |
| 데이터 검증   | Pydantic               |
| 환경변수 관리 | python-dotenv          |

---

## 💡 기존 ML 방식과의 차이점

| 구분                  | 머신러닝 방식     | 이 프로젝트            |
| --------------------- | ----------------- | ---------------------- |
| 학습 데이터           | 수천~수만 개 필요 | **불필요**             |
| 개발 기간             | 수주 이상         | 수 시간                |
| 판단 근거 설명        | 어려움            | **자연어로 설명 가능** |
| 새로운 피싱 패턴 대응 | 재학습 필요       | **즉시 대응**          |

---

## 📋 요구사항

- Python 3.10 이상
- Anthropic API 키 ([발급 바로가기](https://console.anthropic.com))
