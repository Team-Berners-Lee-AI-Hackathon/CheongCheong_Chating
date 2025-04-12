import streamlit as st
from housing_alert.services import db, storage, ai

params = st.query_params

user = params.get("user", None)


st.title("공고 알람")
st.markdown("공고 알람")



