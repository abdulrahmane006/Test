import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="المخازن", layout="centered")

# الستايل المحترف الجديد: توسيط كامل، حواف منحنية، وإلغاء النصوص الجانبية
st.markdown("""
    <style>
    .stApp { direction: RTL; text-align: right; background-color: #ffffff; color: #000000; }
    
    /* تأثير الكيرف المحيط بكلمة المخازن */
    .header-box { text-align: center; margin-top: 5px; margin-bottom: 25px; }
    .shop-title { font-size: 16px; color: #555555; letter-spacing: 2px; margin-bottom: -5px; }
    .main-title { font-size: 36px; font-weight: bold; color: #000000; line-height: 1.1; }
    
    /* جعل حواف خانة البحث منحنية وتغيير محاذاة النص الداخلي */
    div[data-testid="stHeader"], input, .stButton>button, div[data-testid="stExpander"] {
        border-radius: 15px !important;
    }
    .stTextInput>div>div>input {
        text-align: left; /* لجعل النص يظهر يسار الخانة */
        direction: ltr;
    }
    
    /* بطاقة النتيجة المنحنية الموحدة الشاملة لكافة البيانات */
    .unified-card {
        border: 2px solid #000000;
        border-radius: 20px;
        padding: 20px;
        background-color: #ffffff;
        margin-top: 15px;
        text-align: center;
    }
    .center-datetime { font-size: 14px; color: #444444; text-align: center; margin-bottom: 12px; line-height: 1.3; }
    .center-prod-title { font-size: 22px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 15px; }
    
    /* جدول الأعمدة الداخلي الموسط */
    .card-columns { display: flex; justify-content: space-around; margin-top: 10px; text-align: center; }
    .card-col { flex: 1; text-align: center; }
    .col-label { font-size: 14px; color: #777777; margin-bottom: 4px; }
    .col-value { font-size: 18px; font-weight: bold; color: #000000; }
    
    /* تنسيق تبويب آخر الإضافات */
    .stExpander > font { font-size: 20px !important; font-weight: bold; }
    .added-box {
        border: 1px solid #999999;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #ffffff;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if 'products_db' not in st.session_state:
    st.session_state.products_db = pd.DataFrame([
        {"الكود": "101", "اسم النوع": "دم غزال", "اللون": "احمر", "المخزن": "العشة", "العدد المتوفر": 3, "التاريخ": "13/6/2026", "الوقت": "3:39"}
    ])

# الترس أعلى اليمين
top_c1, top_c2 = st.columns([1, 9])
with top_c1:
    st.button("⚙️", key="panel_gear")

# هيدر المحل بتأثير الكيرف الملتف
st.markdown("""
    <div class="header-box">
        <div class="shop-title">محلات زقزوق للأقمشة</div>
        <div class="main-title">المخازن</div>
    </div>
""", unsafe_allow_html=True)
st.write(" ")
# خانة البحث وبداخلها التوجيه العربي جهة الشمال ومسح الجملة السفلية تماًماً
query = st.text_input("", placeholder="(اضغط إدخال)           ", label_visibility="collapsed")

if query:
    df = st.session_state.products_db
    res = df[df['اسم النوع'].str.contains(query, case=False, na=False) | df['الكود'].astype(str).str.contains(query, case=False, na=False)]
    
    if not res.empty:
        for idx, row in res.iterrows():
            # بناء البطاقة المدمجة الموسطة بالكامل وبدون إيموجيز
            st.markdown(f"""
                <div class="unified-card">
                    <div class="center-datetime">{row['التاريخ']}<br>{row['الوقت']}</div>
                    <div class="center-prod-title">{row['اسم النوع']} ({row['الكود']})</div>
                    <hr style="border: 0.5px solid #eeeeee; margin: 10px 0;">
                    <div class="card-columns">
                        <div class="card-col">
                            <div class="col-label">المكان</div>
                            <div class="col-value">{row['المخزن']}</div>
                        </div>
                        <div class="card-col">
                            <div class="col-label">العدد</div>
                            <div class="col-value">{row['العدد المتوفر']}</div>
                        </div>
                        <div class="card-col">
                            <div class="col-label">اللون</div>
                            <div class="col-value">{row['اللون']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center; color:red;'>⚠️ لا توجد نتائج تطابق هذا البحث.</p>", unsafe_allow_html=True)

st.write("---")
# تبويب آخر الإضافات بخط كبير وموسط وبدون إيموجي
with st.expander("آخر الإضافات"):
    if not st.session_state.products_db.empty:
        for idx, row in st.session_state.products_db.iterrows():
            st.markdown(f"""
                <div class="added-box">
                    <div class="center-datetime" style="font-size: 13px; color: #666666;">
                        {row['التاريخ']}<br>{row['الوقت']}
                    </div>
                    <div style="font-size: 20px; font-weight: bold; margin-top: 5px;">{row['اسم النوع']}</div>
                    <div style="font-size: 15px; color: #444444; margin-top: 2px;">({row['الكود']})</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='text-align:center;'>لا توجد إضافات حالياً.</p>", unsafe_allow_html=True)
        

