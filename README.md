# 🏠 New Housing Drawing Notification AI

A smart notifier for youth housing applications.  
Get alerts only for the applications you're eligible for, and ask questions using GenAI (Bedrock / Upstage).

---

## 🚀 Quick Start

```bash
APP_DIR=/opt/housing-alert
git clone https://github.com/Team-Berners-Lee-AI-Hackathon/CheongCheong_Chating.git "$APP_DIR"
cd "$APP_DIR/application"

cat > .env <<'EOF'
AWS_REGION=us-east-1
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-v2
UPSTAGE_API_KEY=replace_me
S3_BUCKET=housing-alert-notices
DYNAMO_USER_TABLE=HousingAlertUsers
DYNAMO_NOTICE_TABLE=HousingAlertNotices
EOF

poetry install
export PYTHONPATH=$PWD/src
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

![user](images/main.png)

### Housing Notice Chat (Q&A)  

![chat](images/chatting.png)

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
