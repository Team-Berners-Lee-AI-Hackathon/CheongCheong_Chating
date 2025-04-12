sudo touch /var/lob/hackathon_app.log
chmod 666 /var/lob/hackathon_app.log

poetry env use "$(pyenv which python)"
poetry install --no-root
export PYTHONPATH=$PWD/src
poetry run streamlit run src/housing_alert/streamlit_app.py