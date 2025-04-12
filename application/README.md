#TODO
- [ ] 예산범위를 전세, 월세, 보증금 으로 세분화
- [ ] 역세권 여부
- [ ] 근처 편의시설  
  - [ ] 헬스장
  - [ ] 공원
  - [ ] 응급실
  - [ ] 대형마트

cd /opt/housing-alert/application
export PYTHONPATH=$PWD/src
poetry run streamlit run src/housing_alert/streamlit_app.py