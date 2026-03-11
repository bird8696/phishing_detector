import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail 읽기 + 수정 권한
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():
    """Gmail API 서비스 객체 반환 (최초 실행 시 브라우저 인증)"""
    creds = None

    # 이전에 인증한 토큰이 있으면 불러오기
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 토큰이 없거나 만료됐으면 새로 인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # 토큰 저장 (다음 실행 시 재사용)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_recent_emails(count: int = 5):
    """최근 이메일 가져오기"""
    service = get_gmail_service()

    # 받은편지함에서 최근 이메일 목록 가져오기
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=count
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        # 이메일 상세 내용 가져오기
        detail = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = detail["payload"]["headers"]

        # 제목, 발신자 추출
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        sender  = next((h["value"] for h in headers if h["name"] == "From"), "")

        # 본문 추출
        body = ""
        payload = detail["payload"]

        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data", "")
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break
        elif "body" in payload:
            data = payload["body"].get("data", "")
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        emails.append({
            "id": msg["id"],       # 메일 이동에 필요한 ID
            "sender": sender,
            "subject": subject,
            "body": body[:1000]    # 너무 길면 앞 1000자만
        })

    return emails, service  # service도 같이 반환 (라벨 작업에 필요)


def get_or_create_label(service, label_name: str = "📁 피싱의심") -> str:
    """피싱의심 라벨이 없으면 생성하고 라벨 ID 반환"""

    # 기존 라벨 목록 가져오기
    labels = service.users().labels().list(userId="me").execute()
    for label in labels.get("labels", []):
        if label["name"] == label_name:
            return label["id"]  # 이미 있으면 ID 반환

    # 없으면 새로 생성
    new_label = service.users().labels().create(
        userId="me",
        body={"name": label_name}
    ).execute()

    return new_label["id"]


def move_to_phishing(service, message_id: str, label_id: str):
    """이메일을 피싱의심 폴더로 이동"""
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "addLabelIds": [label_id],    # 피싱의심 라벨 추가
            "removeLabelIds": ["INBOX"]   # 받은편지함에서 제거
        }
    ).execute()