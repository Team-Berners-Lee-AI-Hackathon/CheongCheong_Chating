# 🛠️ [New Housing Drawing Notification AI] #TODO 추가 필요

### 📌 Overview

This project was developed as part of the Document Based Application Hackathon. It aims to solve the complex and overwhelming process of finding and applying for youth housing by providing targeted notifications and an intelligent Q&A interface using GenAI Bedrock.

### 🚀 Key Features

- ✅ **Smart Notifications**: Receive alerts only for housing applications that match your eligibility criteria.
- ✅ **Automated Workflows**: Seamless integration of crawling, OCR, and information extraction to keep you updated with the latest announcements.
- ✅ **Intelligent Q&A**: Interact with a chatbot powered by GenAI Bedrock for detailed answers about application details such as eligibility and deadlines.

### 🖼️ Demo / Screenshots

- **User Input Interface**  
  ![UserInput](imgs/user_input_demo.png)
- **Chatting Interface**  
  ![Chatting](imgs/chatting_demo.png)
- **Workflow Diagrams**:  
  - 🤖 Crawling: ![Crawling](imgs/crawling.png)  
  - 🔔 Notification: ![Notification](imgs/notification.png)  
  - ⌨️ User Input: ![User Input](imgs/user_input.png)  
  - 💬 Chatting: ![Chatting](imgs/chatting.png)

### 🧩 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python (managed via Poetry)  
- **Database**: DynamoDB  
- **Crawling & Automation**: Selenium, AWS EC2 & Lambda  
- **AI Services**: Upstage API and GenAI Bedrock  
- **Others**: SMTP Protocol for email notifications, AWS S3 for storage, AWS EventBridge for monitoring

### 🏗️ Project Structure
```
📁 #TODO 추가필요
├── application
│   ├── application_python_init.sh
│   ├── korea_regions.json
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── README.md
│   ├── src
│   │   └── housing_alert
│   │       ├── __init__.py
│   │       ├── config.py
│   │       ├── services
│   │       │   ├── __init__.py
│   │       │   ├── ai.py
│   │       │   └── db.py
│   │       └── streamlit_app.py
│   ├── start.sh
│   └── user_data.sh
├── data_collect
│   ├── crawler.py
│   ├── setting.sh
│   ├── Subway.csv
│   ├── 서울시 공공도서관 현황정보.csv
│   ├── 서울시 응급실 위치 정보.csv
│   ├── 서울시 체력단련장업 인허가 정보.csv
│   ├── 서울특별시_하천이용시설 현황_20240906.csv
│   └── 전국초중등학교위치표준데이터.csv
├── images
├── imgs
│   ├── chatting_demo.png
│   ├── chatting.png
│   ├── crawling.png
│   ├── lagacy-main.png
│   ├── lagacy.png
│   ├── notification.png
│   ├── user_input_demo.png
│   └── user_input.png
├── lambda
│   ├── notification
│   │   └── main.py
│   └── pdf_processor
│       └── main.py
├── README.md
└── test
    ├── crawler.py
    ├── data
    │   ├── korea_regions_hierarchical.json
    │   ├── korea_regions.json
    │   ├── parse_regions.py
    │   └── 국토교통부_전국 법정동_20240802.csv
    ├── data2
    │   ├── filtered_cities.json
    │   ├── korea_regions_hierarchical.json
    │   ├── korea_regions.json
    │   ├── normalized_cities.json
    │   ├── parser.py
    │   └── simplified_cities.json
    └── s3_upload_test.sh
```

### 🔧 Setup & Installation

```bash
# Clone the repository: #TODO 수정필요
git clone https://github.com/Team-Berners-Lee-AI-Hackathon/CheongCheong_Chating.git
cd CheongCheong_Chating/application

# Create the environment configuration file
cat > .env <<'EOF'
AWS_REGION=us-east-1
BEDROCK_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0
S3_BUCKET=minerva-1-pdf-bucket
DYNAMO_USER_TABLE=minerva-1-user-info-table
DYNAMO_NOTICE_TABLE=minerva-1-pdf-info-table
EOF

# Install dependencies

poetry install

# Run the Streamlit app

export PYTHONPATH=$PWD/src
poetry run streamlit run src/housing_alert/streamlit_app.py
```

### 📁 Dataset & References

- **Dataset used**: Public housing announcement PDFs collected from government websites (e.g., LH, SH) and processed using OCR.
- **References / Resources**:  
  - [Streamlit Documentation](https://docs.streamlit.io/)  
  - [AWS Documentation](https://docs.aws.amazon.com/)  
  - [Upstage API Documentation](https://www.upstage.ai/)

### 🙌 Team Members

| Name        | Role               | GitHub                                             |
|-------------|--------------------|----------------------------------------------------|
| Bohyun Choi | Project Manager    | [@Brilly-Bohyun](https://github.com/Brilly-Bohyun) |
| Jiwoo Kim   | Backend Developer  | [@WiseWoo](https://github.com/WiseWoo)             |
| Woobin Hwang| AI Developer       | [@binhao22](https://github.com/binhao22)           |
| Hoejung Kim | Backend Developer  | [@hjk1996](https://github.com/hjk1996)             |
| Taeji Kim   | Frontend Developer | [@KKamJi98](https://github.com/KKamJi98)           |

### ⏰ Development Period

- Last updated: 2025-04-13

### 📄 License

This project is licensed under the [MIT license](https://opensource.org/licenses/MIT).  
See the LICENSE file for more details.

### 💬 Additional Notes

- Ensure that AWS credentials are properly configured via `~/.aws/credentials` or system environment variables.
- For any issues or further details, please refer to the documentation in the `/docs` directory or contact the development team.

#TODO 추가필요

