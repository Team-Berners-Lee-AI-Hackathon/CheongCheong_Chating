# ========================= services/ai.py =========================
"""Bedrock & Upstage API 래퍼 – logging & 명시적 에러 반환."""
from typing import List, Dict
import json, os, logging, requests
from housing_alert.config import settings

log = logging.getLogger(__name__)

# ---------- Bedrock ---------- #
# BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
MODEL_ID = settings.BEDROCK_MODEL_ID or "anthropic.claude-3-7-sonnet-20250219-v1:0"

try:
    import boto3

    brt = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
except Exception as e:
    log.exception("Bedrock client 초기화 실패")
    brt = None


def _claude_prompt(user_text: str) -> str:
    return f"\n\nHuman: {user_text}\n\nAssistant:"


def bedrock_chat(messages: List[Dict[str, str]]) -> str:
    if not brt:
        return "[Bedrock 연결 안 됨]"

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
    })

    try:
        resp = brt.invoke_model(
            inferenceProfileArn="arn:aws:bedrock:us-east-1:730335373015:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=body,
            accept="application/json",
            contentType="application/json",
        )
        data = json.loads(resp["body"].read())
        return data.get("content", [{}])[0].get("text", "[빈 응답]")
    except Exception as e:
        log.exception("Bedrock invoke_model 실패")
        return f"[Bedrock Error] {e}"


# ---------- Upstage ---------- #
UPSTAGE_QA_URL = os.getenv("UPSTAGE_QA_ENDPOINT", "https://api.upstage.ai/v1/qa")


def upstage_qa(document: str, question: str) -> str:
    """Upstage 문서 QA – 예외·404 시 에러 문자열 반환."""
    if not settings.UPSTAGE_API_KEY:
        return "[Upstage Error] API KEY 미설정"

    headers = {"Authorization": f"Bearer {settings.UPSTAGE_API_KEY}"}
    try:
        resp = requests.post(
            UPSTAGE_QA_URL,
            json={"document": document, "question": question},
            headers=headers,
            timeout=30,
        )
        if resp.status_code == 404:
            msg = "404 page not found"
            log.error("Upstage 404: %s", msg)
            return f"[Upstage Error] {msg}"
        resp.raise_for_status()
        return resp.json().get("answer", "[Upstage Error] 빈 응답")
    except Exception as e:
        log.exception("Upstage QA 호출 실패")
        return f"[Upstage Error] {e}"
