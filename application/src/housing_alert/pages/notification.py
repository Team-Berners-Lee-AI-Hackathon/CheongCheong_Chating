import streamlit as st
from housing_alert.services import db, storage, ai
from typing import Dict, Any, Optional

params = st.query_params

user_id = params.get("user_id", None)

notifications: Optional[Dict[str, Any]] = db.get_notifications(user_id=user_id)

st.title("공고 알람")

if notifications:
    for i, item in enumerate(notifications):
        with st.container():
            st.subheader(f"알림 {i + 1}")
            announcement_name = item.get("announcement_name", "제목 없음")
            announcement_id = item.get("announcement_id", "")
            link = f"/?user_id={user_id}&announcement_id={announcement_id}"
            st.markdown(f"[{announcement_name}]({link})", unsafe_allow_html=True)
            st.markdown("---")  # 구분선
else:
    st.info("알림이 없습니다.")
