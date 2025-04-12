# ========================= services/ai.py =========================
"""Bedrock & Upstage API 래퍼 – logging & 명시적 에러 반환."""
from typing import List, Dict
import json, os, logging, requests
from housing_alert.config import settings

log = logging.getLogger(__name__)

# ---------- Bedrock ---------- #
# BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
MODEL_ID = settings.BEDROCK_MODEL_ID or "anthropic.claude-3-5-sonnet-20240620-v1:0"

try:
    import boto3

    # Knowledge Bases 클라이언트로 변경
    brt = boto3.client("bedrock-agent-runtime", region_name=BEDROCK_REGION)
except Exception as e:
    log.exception("Bedrock 클라이언트 초기화 실패")
    brt = None


def _claude_prompt(user_text: str) -> str:
    return f"\n\nHuman: {user_text}\n\nAssistant:"

# 사용자 정의 프롬프트 템플릿
prompt_template = """
Use the following search results and user detail to answer the user's question, 사용자한 질문에 대해 모호한 대답은 하지 말고 확실한 대답만 해. 충분한 시간을 갖고 10번을 생각한 뒤 최선의 답변을 하도록 해: 
$search_results$
$user_detail$

Question: $question$
Answer:
"""

def bedrock_chat(user_query: str, user_detail) -> str:
    custom_prompt = prompt_template.format(user_detail=user_detail)
    if not brt:
        return "[Bedrock 연결 안 됨]"
    
    try:
        resp = brt.retrieve_and_generate(
            input={"text": user_query},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": "SUAWIGMKPU",
                    "modelArn": "arn:aws:bedrock:us-east-1:730335373015:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {"numberOfResults": 1}
                    },
                    "generationConfiguration": {
                        "promptTemplate": {"textPromptTemplate": f"{user_detail}+{custom_prompt}"}

                    }
                },
            },
            # retrieveAndGenerateConfiguration={
            #     "type": "EXTERNAL_SOURCES",
            #     "externalSourcesConfiguration": {
            #         'modelArn': 'arn:aws:bedrock:us-east-1:730335373015:foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0',
            #         'sources': [
            #             {
            #                 "sourceType": "S3",
            #                 "s3Location": {
            #                     "uri": "s3://minerva-1-pdf-bucket/b6483633-2e88-4cff-a216-90d482067340.pdf"
            #                 }
            #             }
            #         ]
            #     }
            # },
            # modelArn=f"arn:aws:bedrock:{BEDROCK_REGION}:730335373015:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0",
            # modelArn=f"arn:aws:bedrock:{BEDROCK_REGION}:730335373015:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0",
        )
        print(f"resp => {resp}")
        return resp.get("output", {}).get("text", "[빈 응답]")
    except Exception as e:
        log.exception("Bedrock Knowledge Base 호출 실패")
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
