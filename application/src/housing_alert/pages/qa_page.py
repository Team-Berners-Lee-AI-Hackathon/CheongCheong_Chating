import streamlit as st
from housing_alert.services import db, storage, ai


def show(user_id, notice_id):
    st.set_page_config(page_title="Housing Alert", page_icon="🏠", layout="wide")

    user = db.get_user(user_id)
    notice = db.get_notice(notice_id)

    if not (user and notice):
        st.error("사용자 또는 공고 정보를 찾을 수 없습니다.")
        st.stop()

    st.title(f"🏠 {notice.get('title', '청약 공고')} – Q&A")

    if notice.get("pdf_s3_key"):
        pdf_url = storage.create_presigned_url(notice["pdf_s3_key"])
        if pdf_url:
            st.markdown(f"[📄 공고문 PDF 다운로드]({pdf_url})")

    if notice.get("source_url"):
        st.markdown(f"[🌐 원문 사이트로 이동]({notice['source_url']})")

    st.markdown("---")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # 과거 메시지 출력
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    prompt = st.chat_input("공고에 대해 궁금한 점을 물어보세요…")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- Upstage → Bedrock fallback ---
        answer = ai.upstage_qa(document=notice.get("ocr_text", ""), question=prompt)
        if answer.startswith("[Upstage Error"):
            # Upstage 실패 시 Bedrock 호출
            answer = ai.bedrock_chat([{"role": "user", "content": prompt}])

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
