#TODO
- [ ] annual_income => montly로
- [ ] 자동차가 있으면 자동차 가격도
- [ ] 1인 가구인지, 1인 가구가 아니라고 하면 가구 구성원이 몇명인지
cd /opt/housing-alert/application
export PYTHONPATH=$PWD/src
poetry run streamlit run src/housing_alert/streamlit_app.py
