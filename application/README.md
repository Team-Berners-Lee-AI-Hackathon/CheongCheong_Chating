# 🏠 Housing Alert AI

A smart notifier for youth housing applications.  
Get alerts only for the applications you're eligible for, and ask questions using GenAI (Bedrock / Upstage).

---

## 🚀 Quick Start

```bash
poetry install
poetry run streamlit run src/housing_alert/streamlit_app.py
```

---

## ⚙️ Environment Variables

Configure these via `.env` or system environment variables:

| Variable | Description |
|----------|-------------|
| `AWS_REGION` | e.g., `ap-northeast-2` |
| `BEDROCK_REGION` | e.g., `us-east-1` |
| `BEDROCK_MODEL_ID` | e.g., `anthropic.claude-v2` |
| `UPSTAGE_API_KEY` | Upstage document QA API key |
| `S3_BUCKET` | S3 bucket for storing PDFs |
| `DYNAMO_USER_TABLE` | DynamoDB table for users |
| `DYNAMO_NOTICE_TABLE` | DynamoDB table for notices |

> ✅ AWS credentials must be configured via `~/.aws/credentials` or environment variables.

---

## 📸 Screenshots

### User Registration  

![user](main.png)

### Housing Notice Chat (Q&A)  

![chat](chatting.png)

---

## 🧪 Development

- DynamoDB can be replaced with local or mock resources during development.
- Housing notices (PDF) are stored in S3 after OCR.
- Claude (Bedrock) or Upstage API provides Q&A functionality.

---

## 🛠️ Tech Stack

- Python + Streamlit + Poetry
- AWS Bedrock, S3, DynamoDB
- Upstage Document QA API
- OCR preprocessing (external service)
- Real-time notification system via email / messenger
