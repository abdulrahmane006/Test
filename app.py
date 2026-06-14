import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="المخازن - محلات زقزوق", layout="centered")

# تطبيق ستايل الرسمة بالكامل: حواف منحنية، نصوص سوداء، وتنسيق دقيق
st.markdown("""
    <style>
    .stApp { direction: RTL; text-align: right; background-color: #ffffff; color: #000000; }
    /* تنسيق العنوان الرئيسي المسحوب من رسمتك */
    .header-box { text-align: center; margin-top: 10px; margin-bottom: 20px; }
    .main-title { font-size: 28px; font-weight: bold; color: #000000; margin-bottom: 2px; }
    .sub-title { font-size: 18px; color: #555555; }
    /* جعل كل الحواف في الموقع منحنية ودائرية */
    div[data-testid="stForm"], input, .stButton>button, div[data-testid="stExpander"], .stTextInput>div>div {
        border-radius: 15px !important;
    }
    /* ستايل بطاقة نتيجة البحث المنحنية */
    .result-card {
        border: 2px solid #000000;
        border-radius: 20px;
        padding: 15px;
        background-color: #ffffff;
        margin-top: 15px;
    }
    .card-time { font-size: 14px; color: #333333; margin-bottom: 10px; }
    .card-prod { font-size: 20px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 15px; }
    /* ستايل مستطيلات آخر الإضافات المنحنية */
    .added-item {
        border: 1px solid #777777;
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 10px;
        background-color: #fafafa;
    }
    </style>
""", unsafe_allow_html=True)

if 'products_db' not in st.session_state:
    st.session_state.products_db = pd.DataFrame([
        {"الكود": "101", "اسم النوع": "دم غزال", "اللون": "أحمر غامق", "المخزن": "الرف العلوي", "العدد المتوفر": 55, "التاريخ": "13/6/2026", "الوقت": "3:39"}
    ])

# الترس أعلى اليمين (سنخصص وظيفته لاحقاً بناءً على طلبك)
top_c1, top_c2 = st.columns([1, 9])
with top_c1:
    st.button("⚙️", key="settings_btn")

# هيدر المحل والعنوان في المنتصف
st.markdown("""
    <div class="header-box">
        <div class="main-title">المخازن</div>
        <div class="sub-title">محلات زقزوق للأقمشة</div>
    </div>
""", unsafe_allow_html=True)
st.write(" ")
# خانة البحث (ابحث) الخالية تماماً من الكلمات التوجيهية بالداخل
query = st.text_input("", placeholder="ابحث...", label_visibility="collapsed")

if query:
    df = st.session_state.products_db
    res = df[df['اسم النوع'].str.contains(query, case=False, na=False) | df['الكود'].astype(str).str.contains(query, case=False, na=False)]
    
    if not res.empty:
        for idx, row in res.iterrows():
            # بناء الانبثاق/البطاقة ذات الحواف المنحنية حسب الرسمة بالظبط
            st.markdown(f"""
                <div class="result-card">
                    <div class="card-time">📅 {row['التاريخ']}<br>🕒 {row['الوقت']}</div>
                    <div class="card-prod">{row['اسم النوع']} ({row['الكود']})</div>
                </div>
            """, unsafe_allow_html=True)
            
            # الـ 3 عواميد أسفل الاسم: اللون - العدد المتوفر - المكان
            col1, col2, col3 = st.columns(3)
            with col1: st.text_input("اللون", value=row['اللون'], disabled=True, key=f"c_{idx}")
            with col2: st.metric(label="العدد المتوفر", value=f"{row['العدد المتوفر']} قطعة")
            with col3: st.text_input("المكان", value=row['المخزن'], disabled=True, key=f"l_{idx}")
    else:
        st.warning("⚠️ لا توجد نتائج.")

st.write("---")
# الزر التفاعلي أسفل البحث "آخر الإضافات"
with st.expander("✨ آخر الإضافات"):
    if not st.session_state.products_db.empty:
        # عرض المنتجات في مستطيلات ذات حواف منحنية (تاريخ ووقت أعلى اليمين، اسم وكود في المنتصف)
        for idx, row in st.session_state.products_db.iterrows():
            st.markdown(f"""
                <div class="added-item">
                    <div style="font-size: 12px; color: #555555; float: left; text-align: left;">
                        📅 {row['التاريخ']}<br>🕒 {row['الوقت']}
                    </div>
                    <div style="clear: both;"></div>
                    <div style="text-align: center; font-size: 18px; font-weight: bold; margin-top: -15px;">
                        {row['اسم النوع']}<br>
                        <span style="font-size: 14px; font-weight: normal; color: #444444;">({row['الكود']})</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("لا توجد إضافات حالياً.")
        

