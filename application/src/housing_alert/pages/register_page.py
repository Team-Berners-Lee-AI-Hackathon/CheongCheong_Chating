import streamlit as st
from uuid import uuid4
from housing_alert.services import db


def show():
    st.set_page_config(page_title="Housing Alert", page_icon="🏠", layout="wide")

    st.title("🏠 청년 주택청약 알림 – 사용자 등록")
    st.markdown(
        "청약 자격·우선순위 계산을 위해 기본 정보를 입력하세요. _(**★ 표시는 필수**)_"
    )

    with st.form("user_form"):
        # ───────── 기본 정보 ─────────
        email = st.text_input("★ 이메일", placeholder="you@example.com")
        birth = st.date_input("★ 생년월일")
        gender = st.selectbox("성별 (선택)", ["미선택", "남성", "여성", "기타"])

        # ───────── 경제 정보 ─────────
        income = st.number_input("★ 연 소득(만원)", min_value=0, step=100)
        total_assets = st.number_input("총 자산(만원)", min_value=0, step=100)

        own_house = st.selectbox("자택 보유 여부", ["무주택", "자가 보유"])
        own_car = st.checkbox("자가용 보유")
        car_value = (
            st.number_input("차량 가액(만원)", min_value=0, step=100) if own_car else 0
        )

        saving_count = st.number_input("청약 통장 납입 횟수", min_value=0, step=1)

        # ───────── 거주·선호 ─────────
        residence = st.text_input("★ 현재 거주지 (시/도)")

        preferred_area = st.number_input(
            "선호 전용면적(㎡)", min_value=0.0, step=1.0, format="%.2f"
        )

        budget_min, budget_max = st.slider(
            "예산 범위(만원)", 0, 100000, (0, 50000), step=500
        )

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
                "annual_income": int(income),
                "total_assets": int(total_assets),
                "own_house": own_house,
                "own_car": own_car,
                "car_value": int(car_value) if own_car else None,
                "saving_count": int(saving_count),
                "residence": residence,
                "preferred_area": float(preferred_area),
                "budget_min": int(budget_min),
                "budget_max": int(budget_max),
            }
        )
        st.success("✅ 저장되었습니다! 이메일로 인증 링크가 발송됩니다.")
        st.write(f"**User ID:** `{user_id}` (개발 중 표시)")
        st.stop()
