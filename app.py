import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="المخازن", layout="centered")

# أسماء الملفات المحلية الثابتة داخل جيت هاب
FILE_MAIN = "main_db.csv"
FILE_OUT = "out_db.csv"

# دالة لقراءة البيانات بأمان
def load_local_data(file_path, default_cols):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            if not df.empty and 'الكود' in df.columns:
                df['الكود'] = df['الكود'].astype(str)
            return df
        except:
            return pd.DataFrame(columns=default_cols)
    else:
        return pd.DataFrame(columns=default_cols)

# حفظ القراءة في الجلسة لمنع التصفير عند الـ Refresh والتنقل
if 'db_main' not in st.session_state:
    st.session_state.db_main = load_local_data(FILE_MAIN, ["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان", "التاريخ", "الوقت"])
if 'db_out' not in st.session_state:
    st.session_state.db_out = load_local_data(FILE_OUT, ["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان", "اسم التسليم", "التاريخ", "الوقت"])

if 'show_admin' not in st.session_state: st.session_state.show_admin = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'del_out_idx' not in st.session_state: st.session_state.del_out_idx = None

# دالة الحفظ الفوري واللحظي في الملفات لتثبيت البيانات للأبد
def save_and_sync(df, target="main"):
    if target == "main":
        df.to_csv(FILE_MAIN, index=False)
        st.session_state.db_main = df
    else:
        df.to_csv(FILE_OUT, index=False)
        st.session_state.db_out = df

# 2. هندسة التصميم بالكامل والحواف المنحنية وتوسيط النصوص
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
    .center-prod-title { font-size: 26px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 15px; }
    
    .card-columns { display: flex; justify-content: space-around; margin-top: 10px; text-align: center; }
    .card-col { flex: 1; text-align: center; }
    .col-label { font-size: 14px; color: #777777; margin-bottom: 4px; }
    .col-value { font-size: 17px; font-weight: bold; color: #000000; }
    
    .stExpanderSummary p { font-size: 22px !important; font-weight: bold !important; text-align: center !important; width: 100%; }
    .added-box { border: 1px solid #999999; border-radius: 15px; padding: 15px; margin-bottom: 10px; text-align: center; background-color: #ffffff; }
    .top-login-wrapper { border: 2px solid #000000; border-radius: 15px; padding: 2px; max-width: 100%; margin: 40px auto; }
    .top-login-wrapper input { border: none !important; box-shadow: none !important; background: transparent; }
    .focus-card-title { border: 2px solid #000000; border-radius: 15px; padding: 10px; font-size: 24px; font-weight: bold; background-color: #ffffff; text-align: center; margin: 15px auto; max-width: 100%; }
    .admin-page-title { font-size: 30px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 20px; }
    label { width: 100%; text-align: center !important; display: block !important; font-weight: bold !important; font-size: 15px !important; }
    .confirm-box { border: 2px dashed red; padding: 15px; border-radius: 15px; margin-top: 10px; text-align: center; background-color: #fff5f5; }
    </style>
""", unsafe_allow_html=True)

# 3. زر الترس العلوي لفتح وإغلاق لوحة التحكم بأمان
top_c1, top_c2 = st.columns([1, 9])
with top_c1:
    if st.button("⚙️", key="panel_gear"):
        if st.session_state.is_admin:
            st.session_state.is_admin = False; st.session_state.show_admin = False; st.rerun()
        else:
            st.session_state.show_admin = not st.session_state.show_admin; st.rerun()

# 🔒 بوابة الدخول للمسؤول بكود 404
if st.session_state.show_admin and not st.session_state.is_admin:
    st.markdown('<div class="top-login-wrapper">', unsafe_allow_html=True)
    pass_in = st.text_input("", type="password", placeholder="ادخل الكود لفتح إدارة المخازن", label_visibility="collapsed")
    if pass_in == "404":
        st.session_state.is_admin = True; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 🛠️ صـفـحـة الـمـسـؤول (إدارة وجرد وتعديل فوري ثابت للأبد)
# -------------------------------------------------------------
elif st.session_state.is_admin:
    st.markdown('<div class="admin-page-title">إدارة المخازن الرقمية</div>', unsafe_allow_html=True)
    st.write("---")
    
    with st.expander("قائمة المهام والإشراف", expanded=True):
        menu_choice = st.selectbox(
            "",
            ["تعديل بيانات المخزن الحالي", "إضافة منتج يدوياً للمخزن", "خيار ملف Excel للمخزن", "📊 عرض جرد كميات الخارج"],
            label_visibility="collapsed"
        )
    
    st.write(" ")
    df_main = st.session_state.db_main
    df_out = st.session_state.db_out

    if menu_choice == "تعديل بيانات المخزن الحالي":
        st.markdown('<div class="focus-card-title">التعديل والازالة للمخزن الرئيسي</div>', unsafe_allow_html=True)
        search_c = st.text_input("", placeholder="ابحث بكود المنتج لتعديله...", label_visibility="collapsed")
        target_idx = df_main[df_main['الكود'].astype(str) == str(search_c)].index if search_c else []
        
        if len(target_idx) > 0:
            idx = target_idx[0]; row = df_main.loc[idx]
            
            st.markdown(f'<div class="focus-card-title">{row["اسم النوع"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="unified-card">', unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            with c1: u_name = st.text_input("النوع", value=row["اسم النوع"], key=f"n_{idx}")
            with c2: u_meters = st.number_input("عدد الامتار", value=float(row.get("عدد الامتار", 0.0)), key=f"m_{idx}")
            with c3: u_qty = st.number_input("العدد", value=int(row.get("العدد", 0)), key=f"q_{idx}")
            with c4: u_store = st.text_input("المكان", value=row.get("المكان", "-"), key=f"l_{idx}")
            
            st.write(" ")
            b1, b2 = st.columns(2)
            with b1:
                if st.button("💾 حفظ وتحديث لحظي ثابت", use_container_width=True):
                    now = datetime.now()
                    df_main.at[idx, "اسم النوع"] = u_name
                    df_main.at[idx, "عدد الامتار"] = u_meters
                    df_main.at[idx, "العدد"] = u_qty
                    df_main.at[idx, "المكان"] = u_store
                    df_main.at[idx, "التاريخ"] = now.strftime("%d/%m/%Y")
                    df_main.at[idx, "الوقت"] = now.strftime("%I:%M").lstrip("0")
                    save_and_sync(df_main, "main")
                    st.success("🎉 تم حفظ التعديل لحظياً بنجاح تام!")
                    st.rerun()
            with b2:
                if st.button("🗑️ إزالة المنتج نهائياً", use_container_width=True):
                    df_main = df_main.drop(idx).reset_index(drop=True)
                    save_and_sync(df_main, "main")
                    st.success("🗑️ تم مسح الصنف وحفظ التغيير فوراً.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu_choice == "إضافة منتج يدوياً للمخزن":
        st.markdown('<div class="focus-card-title">إضافة نوع جديد يدوياً للمخزن الحفظ الثابت</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        with st.form("add_m_form"):
            nc = st.text_input("كود المنتج الجديد:")
            nn = st.text_input("اسم النوع الجديد:")
            c1, c2, c3 = st.columns(3)
            with c1: nm = st.number_input("عدد الأمتار:", min_value=0.0)
            with c2: nq = st.number_input("العدد:", min_value=0, step=1)
            with c3: nl = st.text_input("المكان:")
            
            if st.form_submit_button("➕ تأكيد إضافة البطاقة وحفظها لحظياً", use_container_width=True):
                if nc and nn:
                    now = datetime.now()
                    new_r = {"الكود": str(nc), "اسم النوع": str(nn), "عدد الامتار": nm, "العدد": int(nq), "المكان": str(nl), "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")}
                    df_main = pd.concat([df_main, pd.DataFrame([new_r])], ignore_index=True)
                    save_and_sync(df_main, "main")
                    st.success("✅ تم إضافة المنتج وحفظه بنجاح واستقرار!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu_choice == "خيار ملف Excel للمخزن":
        st.markdown('<div class="focus-card-title">رفع ملف Excel للمخزن الرئيسي الحفظ الثابت</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        up_file = st.file_uploader("اختر ملف الإكسيل:", type=["xlsx", "xls"], label_visibility="collapsed")
        if up_file is not None:
            try:
                up_df = pd.read_excel(up_file)
                req = ["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان"]
                if not [c for c in req if c not in up_df.columns]:
                    if st.button("🚀 تفريغ واعتماد ملف الإكسيل فوراً", use_container_width=True):
                        now = datetime.now()
                        up_df["الكود"] = up_df["الكود"].astype(str)
                        up_df["التاريخ"] = now.strftime("%d/%m/%Y")
                        up_df["الوقت"] = now.strftime("%I:%M").lstrip("0")
                        final_df = up_df[req + ["التاريخ", "الوقت"]]
                        save_and_sync(final_df, "main")
                        st.success("🎉 تم رص البيانات وحفظها بنجاح واشتغلت تمام!")
                        st.rerun()
                else: st.error("أعمدة ملف الإكسيل غير مطابقة للترتيب المطلوبة.")
            except Exception as e: st.error(f"خطأ: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu_choice == "📊 عرض جرد كميات الخارج":
        st.markdown('<div class="focus-card-title">دفتر جرد كميات الخارج والتسليمات (شيت التسليمات)</div>', unsafe_allow_html=True)
        if not df_out.empty:
            for idx, row in df_out.iterrows():
                st.markdown(f"""
                    <div class="added-box">
                        <div class="center-datetime">📅 {row.get('التاريخ', '-')}<br>🕒 {row.get('الوقت', '-')}</div>
                        <div style="font-size: 22px; font-weight: bold; color: red;">{row['اسم النوع']}</div>
                        <div style="font-size: 14px; color: #555555; margin-bottom: 8px;">ملاحظة باسم التسليم: <b>{row.get('اسم التسليم', '-')}</b></div>
                        <div class="card-columns">
                            <div class="card-col"><div class="col-label">الكود</div><div class="col-value">{row['الكود']}</div></div>
                            <div class="card-col"><div class="col-label">عدد الأمتار</div><div class="col-value">{row['عدد الامتار']}</div></div>
                            <div class="card-col"><div class="col-label">العدد الخارج</div><div class="col-value">{row['العدد']}</div></div>
                            <div class="card-col"><div class="col-label">المستودع</div><div class="col-value">{row['المكان']}</div></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.del_out_idx == idx:
                    st.markdown("""<div class="confirm-box"><p style='color:red; font-weight:bold; margin-bottom:10px;'>⚠️ هل أنت متأكد من رغبتك في حذف بطاقة التسليم هذه؟</p></div>""", unsafe_allow_html=True)
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("🔥 نعم، حذف نهائي", key=f"out_yes_{idx}", use_container_width=True):
                            df_out = df_out.drop(idx).reset_index(drop=True)
                            save_and_sync(df_out, "out")
                            st.session_state.del_out_idx = None
                            st.success("🗑️ تم المسح والحفظ لحظياً بنجاح!")
                            st.rerun()
                    with bc2:
                        if st.button("❌ تراجع وإلغاء", key=f"out_no_{idx}", use_container_width=True):
                            st.session_state.del_out_idx = None; st.rerun()
                else:
                    if st.button(f"🗑️ إزالة بطاقة التسليم ({row['اسم النوع']})", key=f"out_del_btn_{idx}", use_container_width=True):
                        st.session_state.del_out_idx = idx; st.rerun()
        else: st.info("شيت التسليمات فارغ حالياً.")

    st.write("---")
    if st.button("🚪 خروج والعودة لواجهة العمال الرئيسية", use_container_width=True):
        st.session_state.is_admin = False; st.session_state.show_admin = False; st.rerun()

# -------------------------------------------------------------
# 🏠 الـواجـهـة الـرئـيـسـيـة للمحل (حفظ لحظي فوري آمن للعمال)
# -------------------------------------------------------------
else:
    st.markdown('<div class="header-box"><div class="main-title">المخازن</div><div class="shop-title">محلات زقزوق للأقمشة</div></div>', unsafe_allow_html=True)
    app_page = st.radio("", ["🖥️ عرض بيانات المخزن", "📤 تسجيل الخارج من المخزن"], horizontal=True, label_visibility="collapsed")
    st.write("---")

    df_main = st.session_state.db_main
    df_out = st.session_state.db_out

    if app_page == "🖥️ عرض بيانات المخزن":
        query = st.text_input("", placeholder="ابحث هنا باسم الخامة أو بالكود واضغط Enter...", label_visibility="collapsed")
        if query and not df_main.empty:
            res = df_main[df_main['اسم النوع'].str.contains(query, case=False, na=False) | df_main['الكود'].astype(str).str.contains(query, case=False, na=False)]
            if not res.empty:
                for idx, row in res.iterrows():
                    st.markdown(f"""
                        <div class="unified-card">
                            <div class="center-datetime">{row.get('التاريخ', '15/06/2026')}<br>{row.get('الوقت', '03:00')}</div>
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
            else: st.markdown("<p style='text-align:center; color:red; font-weight:bold;'>⚠️ لا توجد نتائج تطابق هذا البحث.</p>", unsafe_allow_html=True)
        st.write("---")
        with st.expander("آخر الإضافات في المخزن"):
            if not df_main.empty:
                for idx, row in df_main.iterrows():
                    st.markdown(f'<div class="added-box"><div style="font-size: 20px; font-weight: bold;">{row["اسم النوع"]} (كود: {row["الكود"]})</div></div>', unsafe_allow_html=True)

    elif app_page == "📤 تسجيل الخارج من المخزن":
        st.markdown('<div class="focus-card-title">تسجيل قماش خارج من المخزن</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        with st.form("out_form_main", clear_on_submit=True):
            out_code = st.text_input("كود المنتج الخارِج:")
            out_name = st.text_input("اسم النوع الخارِج:")
            c1, c2, c3 = st.columns(3)
            with c1: out_meters = st.number_input("عدد الأمتار الخارجة:", min_value=0.0)
            with c2: out_qty = st.number_input("العدد الخارِج:", min_value=0, step=1)
            with c3: out_loc = st.text_input("المكان المستلم منه:")
            out_receiver = st.text_input("ملاحظة باسم التسليم:")
            
            st.write(" ")
            if st.form_submit_button("🚀 تأكيد تسجيل الخروج وحفظ العملية فوراً", use_container_width=True):
                if out_code and out_name and out_receiver:
                    now = datetime.now()
                    new_out = {"الكود": str(out_code), "اسم النوع": str(out_name), "عدد الامتار": out_meters, "العدد": int(out_qty), "المكان": str(out_loc), "اسم التسليم": str(out_receiver), "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")}
                    df_out = pd.concat([df_out, pd.DataFrame([new_out])], ignore_index=True)
                    save_and_sync(df_out, "out")
                    st.success(f"✅ تم حفظ عملية الخارج تلقائياً ولحظياً في السيرفر!")
                else: st.markdown("<p style='text-align:center; color:red;'>⚠️ يرجى إدخال كافة البيانات الأساسية لإتمام الحفظ.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
                
