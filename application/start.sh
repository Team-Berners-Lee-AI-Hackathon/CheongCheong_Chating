poetry env use "$(pyenv which python)"
poetry install --no-root
export PYTHONPATH=$PWD/src
poetry run streamlit run src/housing_alert/streamlit_app.py