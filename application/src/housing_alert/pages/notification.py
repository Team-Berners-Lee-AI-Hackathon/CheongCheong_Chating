import streamlit as st
from housing_alert.services import db, storage, ai
from typing import Dict, Any, Optional

params = st.query_params

user = params.get("user", None)

notifications: Optional[Dict[str, Any]] = db.get_notifications()

st.title("공고 알람")
st.markdown("공고 알람")

if notifications:
    for i, item in enumerate(notifications):
        with st.container():
            st.subheader(f"알림 {i + 1}")
            for key, value in item.items():
                st.markdown(f"**{key}**: {value}")
            st.markdown("---")  # 구분선
else:
    st.info("알림이 없습니다.")
