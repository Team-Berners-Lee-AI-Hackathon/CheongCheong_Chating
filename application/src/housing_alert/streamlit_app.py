"""Streamlit entrypoint – Housing Alert AI (clean UI)"""
import streamlit as st
from uuid import uuid4
from housing_alert.services import db, storage, ai

# ────────────────────────────────────────────────
st.set_page_config(page_title="Housing Alert", page_icon="🏠",
                   layout="wide", initial_sidebar_state="collapsed")

# ------------------ Query params ----------------
params = st.query_params
uid  = params.get("user_id", [None])[0]
nid  = params.get("notice_id", [None])[0]
# ------------------------------------------------

# 전국 시·군·구 사전 예시 ─ 실제 서비스에선 S3·로컬 JSON 로드 권장
# provinces = {"서울특별시": ["강남구","강동구",...], "경기도": ["수원시","성남시",...], ...}
import json, pathlib
provinces = json.loads(pathlib.Path("korea_regions.json").read_text())  # 17개 시·도 · 250여 시·군·구

# =================================================
# 1) 등록 페이지
# =================================================
if not (uid and nid):
    st.title("🏠 청년 주택청약 알림 – 사용자 등록")
    st.caption("★ 는 필수 입력")

    # ---------- ① 기본 정보 ----------
    with st.expander("① 기본 정보", expanded=True):
        colA, colB = st.columns(2)
        with colA:
            email  = st.text_input("★ 이메일", placeholder="you@example.com")
            birth  = st.date_input("★ 생년월일")
        with colB:
            gender = st.selectbox("성별 (선택)", ["미선택", "남성", "여성", "기타"])
            is_student = st.checkbox("현재 대학(원) 재학·휴학 중")

    # ---------- ② 경제 정보 ----------
    with st.expander("② 경제 정보"):
        income        = st.number_input("★ 연 소득(만원)", 0, step=100)
        total_assets  = st.number_input("총 자산(만원)", 0, step=100)
        own_house     = st.radio("주택 보유", ["무주택", "자가 보유"], horizontal=True)
        own_car       = st.checkbox("자가용 보유")
        car_value     = st.number_input("차량 가액(만원)", 0, step=100, disabled=not own_car)
        saving_count  = st.number_input("청약통장 납입 횟수", 0, step=1)

    # ---------- ③ 거주·선호 ----------
    with st.expander("③ 거주·선호"):
        residence      = st.text_input("★ 현재 거주지 (시/도)")
        preferred_area = st.number_input("선호 전용면적(㎡)", 0.0, step=1.0, format="%.1f")

        st.markdown("##### 💰 예산")
        colJ, colR = st.columns(2)
        with colJ:
            budget_jeonse  = st.number_input("전세 예산(만원)", 0, step=500)
            budget_deposit = st.number_input("보증금(만원)", 0, step=100)
        with colR:
            budget_monthly = st.number_input("월세 예산(만원)", 0, step=5)

        near_subway = st.checkbox("역세권(도보 10분)")

    # ---------- ④ 편의시설 ----------
    with st.expander("④ 근처 편의시설(선택)"):
        col1, col2 = st.columns(2)
        with col1:
            has_gym  = st.checkbox("헬스장")
            has_park = st.checkbox("공원")
        with col2:
            has_er   = st.checkbox("응급실")
            has_mart = st.checkbox("대형마트")

    # ---------- ⑤ 선호 지역(다중) ----------
    with st.expander("⑤ 선호 지역(복수 선택)", expanded=False):
        # ❶ 전국 시·도·군·구 로드
        import json, pathlib
        regions_path = pathlib.Path("korea_regions.json")   # ← JSON 경로
        provinces_all = json.loads(regions_path.read_text())

        # ❷ 시·도 다중 선택
        selected_provinces = st.multiselect(
            "선호 시/도 선택 (다중)",
            list(provinces_all.keys()),
            placeholder="예: 서울특별시, 경기도 …",
        )

        # ❸ 시/군/구 다중 선택 (선택된 시·도에 대해)
        preferred_regions = {}
        if selected_provinces:
            st.markdown("##### 세부 시·군·구 선택")
            for p in selected_provinces:
                sub_opts = provinces_all[p]["direct"]
                # + (옵션) 시 단위 내부 구·출장소
                for city, gu_list in provinces_all[p]["city"].items():
                    sub_opts.extend([f"{city} {g}" for g in gu_list])

                chosen = st.multiselect(f"  {p}", sub_opts, key=f"ms_{p}")
                preferred_regions[p] = chosen

    # ---------- 저장 ----------
    if st.button("저장", type="primary"):
        if not email:
            st.error("이메일은 필수입니다.")
            st.stop()

        uid = str(uuid4())
        db.save_user({
            "user_id": uid,
            "email": email,
            "birth": birth.isoformat(),
            "gender": gender if gender != "미선택" else None,
            "is_student": is_student,
            # 경제
            "annual_income": int(income),
            "total_assets": int(total_assets),
            "own_house": own_house,
            "own_car": own_car,
            "car_value": int(car_value) if own_car else None,
            "saving_count": int(saving_count),
            # 거주·선호
            "residence": residence,
            "preferred_area": float(preferred_area),
            "budget_jeonse": int(budget_jeonse),
            "budget_deposit": int(budget_deposit),
            "budget_monthly": int(budget_monthly),
            "near_subway": near_subway,
            # 편의시설
            "facility_gym": has_gym,
            "facility_park": has_park,
            "facility_er": has_er,
            "facility_mart": has_mart,
            # 선호 지역
            "preferred_regions": preferred_regions,
            "preferred_provinces": selected_provinces,
        })
        st.success(f"✅ 저장 완료! User ID: {uid}")
        st.stop()

# =================================================
# 2) Q&A 페이지
# =================================================
else:
    user   = db.get_user(uid)
    notice = db.get_notice(nid)
    if not (user and notice):
        st.error("사용자 또는 공고 정보를 찾을 수 없습니다.")
        st.stop()

    st.title(f"🏠 {notice.get('title','청약 공고')} – Q&A")

    if notice.get("pdf_s3_key"):
        url = storage.create_presigned_url(notice["pdf_s3_key"])
        st.markdown(f"[📄 PDF 다운로드]({url})")

    if notice.get("source_url"):
        st.markdown(f"[🌐 원문 보기]({notice['source_url']})")

    st.divider()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    q = st.chat_input("공고에 대해 질문해 보세요…")
    if q:
        st.session_state.messages.append({"role":"user","content":q})
        with st.chat_message("user"): st.markdown(q)

        a = ai.upstage_qa(notice.get("ocr_text",""), q) \
            or ai.bedrock_chat([{"role":"user","content":q}])

        st.session_state.messages.append({"role":"assistant","content":a})
        with st.chat_message("assistant"): st.markdown(a)