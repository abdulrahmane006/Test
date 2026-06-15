import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="المخازن", layout="centered")

# تطبيق ستايل الحواف المنحنية والتوسيط الكامل للأرقام والنصوص
st.markdown("""
    <style>
    .stApp { direction: RTL; text-align: right; background-color: #ffffff; color: #000000; }
    .header-box { text-align: center; margin-top: 5px; margin-bottom: 25px; }
    .main-title { font-size: 38px; font-weight: bold; color: #000000; line-height: 1.0; }
    .shop-title { font-size: 16px; color: #555555; margin-top: 5px; }
    input, .stButton>button, div[data-testid="stExpander"], .stSelectbox>div>div { 
        border-radius: 15px !important; text-align: center !important;
    }
    input[type="number"], .stTextInput input { text-align: center !important; }
    .unified-card { border: 2px solid #000000; border-radius: 20px; padding: 20px; background-color: #ffffff; margin-top: 15px; text-align: center; }
    .center-datetime { font-size: 14px; color: #444444; text-align: center; margin-bottom: 12px; line-height: 1.3; }
    .center-prod-title { font-size: 26px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    .card-columns { display: flex; justify-content: space-around; margin-top: 10px; text-align: center; }
    .card-col { flex: 1; text-align: center; }
    .col-label { font-size: 14px; color: #777777; margin-bottom: 4px; }
    .col-value { font-size: 18px; font-weight: bold; color: #000000; }
    .stExpanderSummary p { font-size: 22px !important; font-weight: bold !important; text-align: center !important; width: 100%; }
    .added-box { border: 1px solid #999999; border-radius: 15px; padding: 15px; margin-bottom: 10px; text-align: center; }
    .top-login-wrapper { border: 2px solid #000000; border-radius: 15px; padding: 2px; margin: 20px auto; }
    .top-login-wrapper input { border: none !important; box-shadow: none !important; background: transparent; }
    .focus-card-title { border: 2px solid #000000; border-radius: 15px; padding: 10px; font-size: 24px; font-weight: bold; text-align: center; margin: 15px auto; }
    .admin-page-title { font-size: 30px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 20px; }
    label { width: 100%; text-align: center !important; display: block !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# ربط الأبليكيشن برابط شيت محلات زقزوق الخاص بك فورياً لإجراء التعديلات اللحظية
SHEET_ID = "15Rj3WcnZwaEu2laGCHbx9smky3VFmimK68q0trbCS0M"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

def get_sheet_data():
    try:
        df = pd.read_csv(CSV_URL)
        df['الكود'] = df['الكود'].astype(str)
        return df
    except:
        # جدول احترافي افتراضي بالأعمدة الجديدة لو الشيت واجه مشكلة اتصال مؤقتة
        return pd.DataFrame(columns=["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان", "التاريخ", "الوقت"])

if 'db_main' not in st.session_state: st.session_state.db_main = get_sheet_data()
if 'db_out' not in st.session_state: st.session_state.db_out = pd.DataFrame(columns=["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان", "اسم التسليم", "التاريخ", "الوقت"])
if 'show_admin' not in st.session_state: st.session_state.show_admin = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# زر الترس لفتح بوابتك السرية
t_c1, t_c2 = st.columns([1, 9])
with t_c1:
    if st.button("⚙️"):
        if st.session_state.is_admin:
            st.session_state.is_admin = False; st.session_state.show_admin = False; st.rerun()
        else:
            st.session_state.show_admin = not st.session_state.show_admin; st.rerun()
            if st.session_state.show_admin and not st.session_state.is_admin:
    st.markdown('<div class="top-login-wrapper">', unsafe_allow_html=True)
    pass_in = st.text_input("", type="password", placeholder="ادخل الكود", label_visibility="collapsed")
    if pass_in == "404":
        st.session_state.is_admin = True; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"><div class="main-title">المخازن</div><div class="shop-title">محلات زقزوق للأقمشة</div></div>', unsafe_allow_html=True)
app_page = st.radio("", ["🖥️ عرض بيانات المخزن", "📤 تسجيل الخارج من المخزن"], horizontal=True, label_visibility="collapsed")
st.write("---")

# 🖥️ عرض المخزن الحالي: تم عزل الكود ليظهر الاسم وحده كخامة مع ترتيب الأعمدة الجديد
if app_page == "🖥️ عرض بيانات المخزن" and not st.session_state.is_admin:
    query = st.text_input("", placeholder="(اضغط إدخال)           ", label_visibility="collapsed")
    df = st.session_state.db_main
    if query:
        res = df[df['اسم النوع'].str.contains(query, case=False, na=False) | df['الكود'].astype(str).str.contains(query, case=False, na=False)]
        if not res.empty:
            for idx, row in res.iterrows():
                st.markdown(f"""
                    <div class="unified-card">
                        <div class="center-datetime">{row.get('التاريخ', '15/6/2026')}<br>{row.get('الوقت', '3:00')}</div>
                        <div class="center-prod-title">{row['اسم النوع']}</div>
                        <hr style="border: 0.5px solid #eeeeee; margin: 10px 0;">
                        <div class="card-columns">
                            <div class="card-col"><div class="col-label">النوع</div><div class="col-value">{row['اسم النوع']}</div></div>
                            <div class="card-col"><div class="col-label">الكود</div><div class="col-value">{row['الكود']}</div></div>
                            <div class="card-col"><div class="col-label">عدد الامتار</div><div class="col-value">{row['عدد الامتار']}</div></div>
                            <div class="card-col"><div class="col-label">العدد</div><div class="col-value">{row['العدد']}</div></div>
                            <div class="card-col"><div class="col-label">المكان</div><div class="col-value">{row['المكان']}</div></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else: st.markdown("<p style='text-align:center; color:red; font-weight:bold;'>⚠️ لا توجد نتائج تطابق بحثك.</p>", unsafe_allow_html=True)
    st.write("---")
    with st.expander("آخر الإضافات"):
        if not df.empty:
            for idx, row in df.iterrows():
                st.markdown(f'<div class="added-box"><div style="font-size: 20px; font-weight: bold;">{row["اسم النوع"]}</div></div>', unsafe_allow_html=True)
                # 📤 تسجيل الخارج من المخزن: رصد دفتر الخارج المنفصل مع إضافة ملاحظة اسم التسليم
elif app_page == "📤 تسجيل الخارج من المخزن" and not st.session_state.is_admin:
    st.markdown('<div class="focus-card-title">تسجيل قماش خارج من المخزن</div>', unsafe_allow_html=True)
    st.markdown('<div class="unified-card">', unsafe_allow_html=True)
    with st.form("out_form", clear_on_submit=True):
        out_code = st.text_input("كود المنتج الخارِج:")
        out_name = st.text_input("اسم النوع الخارِج:")
        c1, c2, c3 = st.columns(3)
        with c1: out_meters = st.number_input("عدد الأمتار الخارجة:", min_value=0.0)
        with c2: out_qty = st.number_input("العدد الخارِج:", min_value=0, step=1)
        with c3: out_loc = st.text_input("المكان المستلم منه:")
        out_receiver = st.text_input("ملاحظة باسم التسليم:")
        
        if st.form_submit_button("🚀 تأكيد تسجيل الخروج وحفظ العملية", use_container_width=True):
            if out_code and out_name and out_receiver:
                now = datetime.now()
                new_out = {"الكود": str(out_code), "اسم النوع": str(out_name), "عدد الامتار": out_meters, "العدد": int(out_qty), "المكان": str(out_loc), "اسم التسليم": str(out_receiver), "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")}
                st.session_state.db_out = pd.concat([st.session_state.db_out, pd.DataFrame([new_out])], ignore_index=True)
                st.success(f"✅ تم الحفظ وتوثيق التسليم لـ ({out_receiver}) لحظياً!")
            else: st.markdown("<p style='text-align:center; color:red;'>⚠️ يرجى إدخال الكود، الاسم، وملاحظة اسم التسليم.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 🛠️ لوحة إدارة المسؤول: جرد، تعديل، إزالة، ورفع إكسيل المخزن بتنسيق الأعمدة المحدثة
elif st.session_state.is_admin:
    st.markdown('<div class="admin-page-title">إدارة المخازن</div>', unsafe_allow_html=True)
    with st.expander("قائمة المهام", expanded=True):
        menu = st.selectbox("", ["تعديل بيانات المخزن الحالي", "إضافة منتج يدوياً للمخزن", "خيار ملف Excel للمخزن"], label_visibility="collapsed")
    df = st.session_state.db_main

    if menu == "تعديل بيانات المخزن الحالي":
        st.markdown('<div class="focus-card-title">التعديل والازالة</div>', unsafe_allow_html=True)
        search_c = st.text_input("", placeholder="ابحث بكود المنتج لتعديله...", label_visibility="collapsed")
        target_idx = df[df['الكود'].astype(str) == str(search_c)].index if search_c else []
        
        if len(target_idx) > 0:
            idx = target_idx[0]; row = df.loc[idx]
            st.markdown(f'<div class="focus-card-title">{row["اسم النوع"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="unified-card">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1: u_name = st.text_input("النوع", value=row["اسم النوع"], key=f"n_{idx}")
            with c2: u_meters = st.number_input("عدد الامتار", value=float(row.get("عدد الامتار", 0.0)), key=f"m_{idx}")
            with c3: u_qty = st.number_input("العدد", value=int(row.get("العدد", 0)), key=f"q_{idx}")
            with c4: u_store = st.text_input("المكان", value=row.get("المكان", "-"), key=f"l_{idx}")
            
            b1, b2 = st.columns(2)
            with b1:
                if st.button("💾 حفظ وتحديث الوقت", use_container_width=True):
                    now = datetime.now()
                    df.at[idx, "اسم النوع"], df.at[idx, "عدد الامتار"], df.at[idx, "العدد"], df.at[idx, "المكان"] = u_name, u_meters, u_qty, u_store
                    df.at[idx, "التاريخ"], df.at[idx, "الوقت"] = now.strftime("%d/%m/%Y"), now.strftime("%I:%M").lstrip("0")
                    st.session_state.db_main = df; st.success("🎉 تم حفظ التعديل بنجاح!"); st.rerun()
            with b2:
                if st.button("🗑️ إزالة المنتج نهائياً", use_container_width=True):
                    st.session_state.db_main = df.drop(idx).reset_index(drop=True)
                    st.success("🗑️ تم الإزالة."); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "إضافة منتج يدوياً للمخزن":
        st.markdown('<div class="focus-card-title">إضافة نوع جديد يدوياً</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        with st.form("add_m"):
            nc = st.text_input("كود المنتج الجديد:")
            nn = st.text_input("اسم النوع الجديد:")
            c1, c2, c3 = st.columns(3)
            with c1: nm = st.number_input("عدد الأمتار:", min_value=0.0)
            with c2: nq = st.number_input("العدد:", min_value=0, step=1)
            with c3: nl = st.text_input("المكان:")
            if st.form_submit_button("➕ تأكيد إضافة البطاقة وحفظها", use_container_width=True):
                if nc and nn:
                    now = datetime.now()
                    new_r = {"الكود": str(nc), "اسم النوع": str(nn), "عدد الامتار": nm, "العدد": int(nq), "المكان": str(nl), "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")}
                    st.session_state.db_main = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
                    st.success("✅ تم إضافة النوع الجديد للمخازن!"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "خيار ملف Excel للمخزن":
        st.markdown('<div class="focus-card-title">رفع ملف Excel</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#555555; font-weight:bold;'>الأعمدة المطلوبة: الكود | اسم النوع | عدد الامتار | العدد | المكان</p>", unsafe_allow_html=True)
        up_file = st.file_uploader("اختر ملف الإكسيل:", type=["xlsx", "xls"], label_visibility="collapsed")
        if up_file is not None:
            try:
                up_df = pd.read_excel(up_file)
                req = ["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان"]
                if not [c for c in req if c not in up_df.columns]:
                    if st.button("🚀 تفريغ واعتماد ملف الإكسيل وتحويله لبطاقات متتالية", use_container_width=True):
                        now = datetime.now()
                        up_df["التاريخ"], up_df["الوقت"] = now.strftime("%d/%m/%Y"), now.strftime("%I:%M").lstrip("0")
                        st.session_state.db_main = up_df[req + ["التاريخ", "الوقت"]]; st.success("🎉 تم تفريغ الإكسيل بنجاح!"); st.rerun()
                else: st.error("تأكد من مطابقة أسماء الأعمدة في ملف الإكسيل.")
            except Exception as e: st.error(f"خطأ: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    if st.button("🚪 خروج والعودة لواجهة العمال الرئيسية", use_container_width=True):
        st.session_state.is_admin = False; st.session_state.show_admin = False; st.rerun()
        
