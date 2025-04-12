"""Streamlit entrypoint – Housing Alert AI"""

import streamlit as st
from uuid import uuid4

from housing_alert.services import db, storage, ai   # ← 중복 import 제거

st.set_page_config(page_title="Housing Alert", page_icon="🏠", layout="wide")

# ------------------ Query‑params ------------------
params = st.query_params
_first = lambda v: v[0] if isinstance(v, list) else v
user_id   = _first(params.get("user_id")) if params.get("user_id") else None
notice_id = _first(params.get("notice_id")) if params.get("notice_id") else None
# --------------------------------------------------

# ==================================================
# 1) No query‑params  → User‑registration page
# 2) Both params set  → Q&A page
# ==================================================

if not (user_id and notice_id):
    # ---------- 사용자 등록 ----------
    st.title("🏠 청년 주택청약 알림 – 사용자 등록")
    st.markdown(
        "청약 자격·우선순위 계산을 위해 기본 정보를 입력하세요. _(★ 표시는 필수)_"
    )

    with st.form("user_form"):
        # ───────── 기본 정보 ─────────
        email  = st.text_input("★ 이메일", placeholder="you@example.com")
        birth  = st.date_input("★ 생년월일")
        gender = st.selectbox("성별 (선택)", ["미선택", "남성", "여성", "기타"])

        # ───────── 경제 정보 ─────────
        income        = st.number_input("★ 연 소득(만원)", min_value=0, step=100)
        total_assets  = st.number_input("총 자산(만원)", min_value=0, step=100)
        own_house     = st.selectbox("자택 보유 여부", ["무주택", "자가 보유"])
        own_car       = st.checkbox("자가용 보유")
        car_value     = (
            st.number_input("차량 가액(만원)", min_value=0, step=100) if own_car else 0
        )
        saving_count  = st.number_input("청약 통장 납입 횟수", min_value=0, step=1)

        # ───────── 거주·선호 ─────────
        residence      = st.text_input("★ 현재 거주지 (시/도)")
        preferred_area = st.number_input(
            "선호 전용면적(㎡)", min_value=0.0, step=1.0, format="%.2f"
        )

        st.markdown("#### 💰 Budget")
        col_jeonse, col_rent = st.columns(2)
        with col_jeonse:
            budget_jeonse  = st.number_input("전세 예산(만원)", min_value=0, step=500)
            budget_deposit = st.number_input("보증금 예산(만원)", min_value=0, step=100)
        with col_rent:
            budget_monthly = st.number_input("월세 예산(만원)", min_value=0, step=5)

        # ───────── 역세권 여부 ─────────
        near_subway = st.checkbox("역세권(도보 10분 이내)")

        # ───────── 근처 편의시설 ─────────
        st.markdown("#### 🏪 Nearby Facilities (선택)")
        col1, col2 = st.columns(2)
        with col1:
            has_gym  = st.checkbox("헬스장")
            has_park = st.checkbox("공원")
        with col2:
            has_er   = st.checkbox("응급실")
            has_mart = st.checkbox("대형마트")

        submitted = st.form_submit_button("저장")

    if submitted:
        if not email:
            st.error("이메일은 필수입니다.")
            st.stop()

        user_id = str(uuid4())
        db.save_user(
            {
                "user_id": user_id,
                "email": email,
                "birth": birth.isoformat(),
                "gender": gender if gender != "미선택" else None,
                # 경제 정보
                "annual_income": int(income),
                "total_assets": int(total_assets),
                "own_house": own_house,
                "own_car": own_car,
                "car_value": int(car_value) if own_car else None,
                "saving_count": int(saving_count),
                # 거주·선호
                "residence": residence,
                "preferred_area": float(preferred_area),
                # 예산 세분화
                "budget_jeonse": int(budget_jeonse),
                "budget_deposit": int(budget_deposit),
                "budget_monthly": int(budget_monthly),
                # 역세권 + 편의시설
                "near_subway": near_subway,
                "facility_gym": has_gym,
                "facility_park": has_park,
                "facility_er": has_er,
                "facility_mart": has_mart,
            }
        )
        st.success("✅ 저장되었습니다! 이메일로 인증 링크가 발송됩니다.")
        st.write(f"**User ID:** `{user_id}` (개발 중 표시)")
        st.stop()

else:
    # ---------- Q&A 화면 ----------
    user   = db.get_user(user_id)
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
        if answer and answer.startswith("[Upstage Error"):
            answer = ai.bedrock_chat([{"role": "user", "content": prompt}])

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)