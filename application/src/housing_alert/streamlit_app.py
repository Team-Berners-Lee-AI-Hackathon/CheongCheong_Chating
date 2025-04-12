"""Streamlit 엔트리포인트."""

import streamlit as st
from housing_alert.pages import register_page, qa_page

params = st.query_params
_first = lambda v: v[0] if isinstance(v, list) else v
user_id = _first(params.get("user_id")) if params.get("user_id") else None
notice_id = _first(params.get("notice_id")) if params.get("notice_id") else None

if not (user_id and notice_id):
    register_page.show()
else:
    qa_page.show(user_id, notice_id)
