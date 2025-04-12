#TODO
- [ ] 1인 가구인지 -> 아니면 가족 구성원이 몇명인지
cd /opt/housing-alert/application
export PYTHONPATH=$PWD/src
poetry run streamlit run src/housing_alert/streamlit_app.py
