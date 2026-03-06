# 🔐 피싱 이메일 탐지기

Claude AI를 활용해 이메일의 피싱 여부를 자동으로 분석하는 FastAPI 기반 REST API 서버입니다.

---

## 📌 프로젝트 소개

피싱 이메일은 개인정보 탈취, 금융 사기 등에 악용되는 대표적인 사이버 공격입니다.
이 프로젝트는 Anthropic의 **Claude AI** 에게 보안 전문가 역할을 부여하여,
별도의 학습 데이터 없이도 이메일의 피싱 여부를 분석하고 위험도와 대응 방법을 제시합니다.

### 기존 머신러닝 방식과의 차이점

| 구분                  | 머신러닝 방식     | 이 프로젝트            |
| --------------------- | ----------------- | ---------------------- |
| 학습 데이터           | 수천~수만 개 필요 | **불필요**             |
| 개발 기간             | 수주 이상         | 수 시간                |
| 판단 근거 설명        | 어려움            | **자연어로 설명 가능** |
| 새로운 피싱 패턴 대응 | 재학습 필요       | **즉시 대응**          |

---

## ⚙️ 설치 및 실행

### 1. 패키지 설치

```bash
pip install fastapi uvicorn anthropic pydantic python-dotenv
```

### 2. API 키 설정

`.env` 파일에 Anthropic API 키를 입력하세요.

```
ANTHROPIC_API_KEY=여기에_실제_API키_입력
```

> API 키 발급: https://console.anthropic.com

### 3. 서버 실행

```bash
python main.py
```

### 4. 서버 종료

```
Ctrl + C
```

---

## 🖥️ 사용 방법 (Swagger UI)

서버 실행 후 브라우저에서 아래 주소로 접속하세요.

```
http://localhost:8000/docs
```

---

### Step 1. POST /analyze 클릭

화면에서 **`POST /analyze`** 버튼을 클릭해 펼쳐주세요.

---

### Step 2. Try it out 클릭

오른쪽 상단의 **`Try it out`** 버튼을 클릭하세요.

---

### Step 3. 분석할 이메일 입력

아래 형식으로 이메일 내용을 입력하세요.

```json
{
  "sender": "발신자 이메일 주소",
  "subject": "이메일 제목",
  "body": "이메일 본문 내용"
}
```

**입력 예시 (피싱 이메일)**

```json
{
  "sender": "security@kak4o-bank.com",
  "subject": "[긴급] 계정이 잠겼습니다",
  "body": "고객님 24시간 내에 본인인증을 완료하지 않으면 계정이 영구 정지됩니다. 주민등록번호와 계좌번호를 입력해주세요."
}
```

> `sender`(발신자), `subject`(제목)는 선택사항입니다.
> `body`(본문)는 필수입니다.

---

### Step 4. Execute 클릭

**`Execute`** 버튼을 클릭하면 분석이 시작됩니다.

---

### Step 5. 결과 확인

**Response body** 에서 분석 결과를 확인하세요.

```json
{
  "is_phishing": true,
  "risk_level": "HIGH",
  "reason": "발신자 주소 위장 및 긴급성 유도, 개인정보 요구",
  "recommendation": "링크를 클릭하지 말고 즉시 삭제하세요."
}
```

| 항목             | 설명                                      |
| ---------------- | ----------------------------------------- |
| `is_phishing`    | 피싱 여부 (true: 피싱 의심 / false: 정상) |
| `risk_level`     | 위험도 (LOW / MEDIUM / HIGH)              |
| `reason`         | 피싱으로 판단한 근거                      |
| `recommendation` | 권고 행동                                 |

---

## 🗂 프로젝트 구조

```
phishing_detector/
├── main.py                # FastAPI 앱 진입점
├── requirements.txt       # 의존 패키지 목록
├── .env                   # API 키 설정 (GitHub 비공개)
├── models/
│   └── schemas.py         # 요청/응답 데이터 구조
├── routes/
│   └── analyze.py         # API 엔드포인트
└── services/
    └── analyzer.py        # Claude API 분석 로직
```

---

## 🛠 기술 스택

| 역할          | 기술                   |
| ------------- | ---------------------- |
| API 서버      | FastAPI                |
| AI 분석       | Claude API (Anthropic) |
| 데이터 검증   | Pydantic               |
| 환경변수 관리 | python-dotenv          |

## 📋 요구사항

- Python 3.11.9
- Anthropic API 키 ([발급 바로가기](https://console.anthropic.com))
