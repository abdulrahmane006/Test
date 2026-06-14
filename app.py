import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="المخازن - محلات زقزوق", layout="centered")

# 2. تصميم الواجهة بالكامل (الحواف المنحنية، التوسيط، والتنسيق الموحد)
st.markdown("""
    <style>
    .stApp { direction: RTL; text-align: right; background-color: #ffffff; color: #000000; }
    
    /* تنسيق الهيدر للواجهة الرئيسية */
    .header-box { text-align: center; margin-top: 5px; margin-bottom: 25px; }
    .main-title { font-size: 38px; font-weight: bold; color: #000000; line-height: 1.0; }
    .shop-title { font-size: 16px; color: #555555; margin-top: 5px; }
    
    /* جعل كل الحواف في الأزرار والخانات والقوائم منحنية */
    input, .stButton>button, div[data-testid="stExpander"], .stSelectbox>div>div { 
        border-radius: 15px !important; 
    }
    .stTextInput>div>div>input { text-align: left; direction: ltr; }
    
    /* بطاقة النتيجة المنحنية الموحدة الشاملة */
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
    
    /* جدول الأعمدة الموسطة */
    .card-columns { display: flex; justify-content: space-around; margin-top: 10px; text-align: center; }
    .card-col { flex: 1; text-align: center; }
    .col-label { font-size: 14px; color: #777777; margin-bottom: 4px; }
    .col-value { font-size: 18px; font-weight: bold; color: #000000; }
    
    /* تخصيص "آخر الإضافات" وقائمة المهام لتكون موسطة وعريضة */
    .stExpanderSummary p { font-size: 22px !important; font-weight: bold !important; text-align: center !important; width: 100%; }
    .added-box {
        border: 1px solid #999999;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #ffffff;
        text-align: center;
    }
    
    /* تخصيص صندوق الكود السري الموسط المنضبط */
    .login-container {
        border: 2px solid #000000;
        border-radius: 20px;
        padding: 25px;
        max-width: 350px;
        margin: 80px auto;
        text-align: center;
    }
    .login-label { font-size: 20px; font-weight: bold; color: #000000; margin-bottom: 15px; text-align: center; }
    
    /* تصميم بطاقات صفحة المسؤول بدون تداخل */
    .admin-card {
        border: 2px solid #000000;
        border-radius: 20px;
        padding: 20px;
        background-color: #ffffff;
        margin-bottom: 15px;
        text-align: center;
    }
    .admin-page-title { font-size: 26px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 20px; }
    .admin-section-title { font-size: 22px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. قاعدة البيانات الافتراضية
if 'products_db' not in st.session_state:
    st.session_state.products_db = pd.DataFrame([
        {"الكود": "101", "اسم النوع": "دم غزال", "اللون": "احمر", "المخزن": "العشة", "العدد المتوفر": 3, "التاريخ": "13/6/2026", "الوقت": "3:39"}
    ])

if 'show_admin_flow' not in st.session_state:
    st.session_state.show_admin_flow = False
if 'is_admin_logged' not in st.session_state:
    st.session_state.is_admin_logged = False

# 4. الترس أعلى اليمين للتحويل بين الصفحات لقفل الجلسة
top_c1, top_c2 = st.columns([1, 9])
with top_c1:
    if st.button("⚙️", key="panel_gear"):
        if st.session_state.is_admin_logged:
            st.session_state.is_admin_logged = False
            st.session_state.show_admin_flow = False
            st.rerun()
        else:
            st.session_state.show_admin_flow = not st.session_state.show_admin_flow
            st.rerun()

# -------------------------------------------------------------
# 🔒 بـوابـة المسؤول (تظهر فقط عند الضغط على الترس)
# -------------------------------------------------------------
if st.session_state.show_admin_flow and not st.session_state.is_admin_logged:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-label">ادخل الكود</div>', unsafe_allow_html=True)
    pass_in = st.text_input("", type="password", placeholder="اكتب الكود هنا...", label_visibility="collapsed")
    if pass_in == "404":
        st.session_state.is_admin_logged = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 🛠️ صـفـحـة الـمـسـؤول الـمـعـدلة (عند كتابة كود 404 بنجاح)
# -------------------------------------------------------------
elif st.session_state.is_admin_logged:
    st.markdown('<div class="admin-page-title">لوحة تحكم محلات زقزوق</div>', unsafe_allow_html=True)
    st.write("---")
    
    # قائمة المهام في المنتصف كخيار تبويب منبثق منحني وموسط يمنع التداخل
    with st.expander("📋 قائمة المهام"):
        menu_choice = st.selectbox(
            "",
            ["تعديل البيانات الحالية", "إضافة منتج يدوياً", "خيار ملف Excel"],
            label_visibility="collapsed"
        )
    
    st.write(" ")

    # الخانة الأولى: تعديل البيانات الحالية على هيئة بطاقات متتالية موسطة ومنحنية
    if menu_choice == "تعديل البيانات الحالية":
        st.markdown('<div class="admin-section-title">تعديل وجرد البطاقات الحالية يدوياً</div>', unsafe_allow_html=True)
        if not st.session_state.products_db.empty:
            updated_rows = []
            for idx, row in st.session_state.products_db.iterrows():
                st.markdown('<div class="admin-card">', unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:22px; font-weight:bold; margin-bottom:15px;'>{row['اسم النوع']} ({row['الكود']})</div>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                with c1: u_color = st.text_input("اللون", value=row["اللون"], key=f"ec_{idx}")
                with c2: u_qty = st.number_input("العدد", value=int(row["العدد المتوفر"]), min_value=0, step=1, key=f"eq_{idx}")
                with c3: u_store = st.text_input("المكان", value=row["المخزن"], key=f"el_{idx}")
                
                updated_rows.append({
                    "الكود": row["الكود"], "اسم النوع": row["اسم النوع"], 
                    "اللون": u_color, "المخزن": u_store, "العدد المتوفر": u_qty,
                    "التاريخ": row["التاريخ"], "الوقت": row["الوقت"]
                })
                st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("💾 حفظ التعديلات الحالية وتحديث التواريخ", use_container_width=True):
                now = datetime.now()
                final_df = pd.DataFrame(updated_rows)
                for i in range(len(final_df)):
                    old_r = st.session_state.products_db.iloc[i]
                    new_r = final_df.iloc[i]
                    if not (old_r["اللون"] == new_r["اللون"] and old_r["العدد المتوفر"] == new_r["العدد المتوفر"] and old_r["المخزن"] == new_r["المخزن"]):
                        final_df.at[i, "التاريخ"] = now.strftime("%d/%m/%Y")
                        final_df.at[i, "الوقت"] = now.strftime("%I:%M").lstrip("0")
                st.session_state.products_db = final_df
                st.success("✅ تم حفظ التعديلات وتحديث التواريخ تلقائياً!")
                st.rerun()
        else:
            st.info("المخزن فارغ حالياً.")

    # الخانة الثانية: إضافة منتج يدوياً في بطاقة فارغة منحنية
    elif menu_choice == "إضافة منتج يدوياً":
        st.markdown('<div class="admin-section-title">بيانات البطاقة الجديدة</div>', unsafe_allow_html=True)
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        with st.form("add_form_admin", clear_on_submit=True):
            nc = st.text_input("كود المنتج:")
            nn = st.text_input("اسم النوع:")
            c1, c2, c3 = st.columns(3)
            with c1: n_color = st.text_input("اللون:")
            with c2: n_qty = st.number_input("العدد:", min_value=0, step=1)
            with c3: n_store = st.text_input("المكان:")
            
            if st.form_submit_button("➕ تأكيد الحفظ للمخزن", use_container_width=True):
                if nc and nn:
                    now = datetime.now()
                    new_row = {
                        "الكود": str(nc), "اسم النوع": str(nn), "اللون": str(n_color), "المخزن": str(n_store), 
                        "العدد المتوفر": int(n_qty), "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")
                    }
                    st.session_state.products_db = pd.concat([st.session_state.products_db, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("✅ تم إضافة المنتج وتوليد التوقيت تلقائياً!")
                    st.rerun()
                else:
                    st.error("⚠️ يجب كتابة الكود والاسم")
        st.markdown('</div>', unsafe_allow_html=True)

    # الخانة الثالثة: رفع ملف إكسيل وتفريغه لبطاقات متتالية
    elif menu_choice == "خيار ملف Excel":
        st.markdown('<div class="admin-section-title">رفع ملف Excel وتفريغه لبطاقات</div>', unsafe_allow_html=True)
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        st.write("الأعمدة المطلوبة: `الكود` | `اسم النوع` | `اللون` | `المخزن` | `العدد المتوفر`")
        up_file = st.file_uploader("اختر الملف:", type=["xlsx", "xls"])
        if up_file is not None:
            try:
                up_df = pd.read_excel(up_file)
                req = ["الكود", "اسم النوع", "اللون", "المخزن", "العدد المتوفر"]
                if not [c for c in req if c not in up_df.columns]:
                    if st.button("🚀 تفريغ واعتماد الإكسيل فوراً", use_container_width=True):
                        now = datetime.now()
                        up_df["الكود"] = up_df["الكود"].astype(str)
                        up_df["اسم النوع"] = up_df["اسم النوع"].astype(str)
                        up_df["اللون"] = up_df["اللون"].fillna("-").astype(str)
                        up_df["المخزن"] = up_df["المخزن"].fillna("-").astype(str)
                        up_df["العدد المتوفر"] = up_df["العدد المتوفر"].fillna(0).astype(int)
                        up_df["التاريخ"] = now.strftime("%d/%m/%Y")
                        up_df["الوقت"] = now.strftime("%I:%M").lstrip("0")
                        
                        st.session_state.products_db = up_df[req + ["التاريخ", "الوقت"]]
                        st.success("🎉 تم تفريغ الإكسيل بنجاح!")
                        st.rerun()
                else: st.error("تأكد من أسماء الأعمدة في ملف الإكسيل")
            except Exception as e: st.error(f"خطأ: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("---")
    if st.button("🚪 خروج والعودة للرئيسية", use_container_width=True):
        st.session_state.is_admin_logged = False
        st.session_state.show_admin_flow = False
        st.rerun()

# -------------------------------------------------------------
# 🏠 الـواجـهـة الـرئـيـسـيـة للمحل (تظهر للعمال و المرور)
# -------------------------------------------------------------
else:
    st.markdown("""
        <div class="header-box">
            <div class="main-title">المخازن</div>
            <div class="shop-title">محلات زقزوق للأقمشة</div>
        </div>
    """, unsafe_allow_html=True)

    st.write(" ")
    query = st.text_input("", placeholder="(اضغط إدخال)           ", label_visibility="collapsed")

    if query:
        df = st.session_state.products_db
        res = df[df['اسم النوع'].str.contains(query, case=False, na=False) | df['الكود'].astype(str).str.contains(query, case=False, na=False)]
        
        if not res.empty:
            for idx, row in res.iterrows():
                st.markdown(f"""
                    <div class="unified-card">
                        <div class="center-datetime">{row['التاريخ']}<br>{row['الوقت']}</div>
                        <div class="center-prod-title">{row['اسم النوع']} ({row['الكود']})</div>
                        <hr style="border: 0.5px solid #eeeeee; margin: 10px 0;">
                        <div class="card-columns">
                            <div class="card-col">
                                <div class="col-label">اللون</div>
                                <div class="col-value">{row['اللون']}</div>
                            </div>
                            <div class="card-col">
                                <div class="col-label">العدد</div>
                                <div class="col-value">{row['العدد المتوفر']}</div>
                            </div>
                            <div class="card-col">
                                <div class="col-label">المكان</div>
                                <div class="col-value">{row['المخزن']}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center; color:red;'>⚠️ لا توجد نتائج تطابق هذا البحث.</p>", unsafe_allow_html=True)

    st.write("---")

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
            
