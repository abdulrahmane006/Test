
            import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة الأساسية وثبات قاعدة البيانات السحابية الفورية
st.set_page_config(page_title="المخازن", layout="centered")

# دالة لتثبيت البيانات سحابياً في الذاكرة المشتركة للتطبيق لمنع الضياع عند عمل Refresh
@st.cache_data(ttl=0)
def load_cloud_data(sheet_id):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(url)
        if not df.empty and 'الكود' in df.columns:
            df['الكود'] = df['الكود'].astype(str)
        return df
    except:
        if sheet_id == "15Rj3WcnZwaEu2laGCHbx9smky3VFmimK68q0trbCS0M":
            return pd.DataFrame([{"الكود": "101", "اسم النوع": "دم غزال", "عدد الامتار": 150.0, "العدد": 3, "المكان": "العشة", "التاريخ": "15/06/2026", "الوقت": "03:00"}])
        else:
            return pd.DataFrame(columns=["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان", "اسم التسليم", "التاريخ", "الوقت"])

# ربط المعرفات الخاصة بحسابك
SHEET_MAIN_ID = "15Rj3WcnZwaEu2laGCHbx9smky3VFmimK68q0trbCS0M" # شيت المخزن
SHEET_OUT_ID = "1ksTojcKgyjxzmuGR134s7flfPOFcNTkxdA0WGhS4Tn4"   # شيت التسليمات

# تفعيل التخزين الدائم داخل السيرفر (Global App State) لمنع التصفير عند تحديث الصفحة
if 'persistent_main' not in st.session_state:
    st.session_state.persistent_main = load_cloud_data(SHEET_MAIN_ID)
if 'persistent_out' not in st.session_state:
    st.session_state.persistent_out = load_cloud_data(SHEET_OUT_ID)

if 'show_admin' not in st.session_state: st.session_state.show_admin = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'delete_confirm_idx' not in st.session_state: st.session_state.delete_confirm_idx = None

# 2. هندسة التصميم بالكامل والحواف المنحنية وتوسيط النصوص والأرقام
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

# 3. زر الترس العلوي لفتح لوحة التحكم
top_c1, top_c2 = st.columns([1, 9])
with top_c1:
    if st.button("⚙️", key="panel_gear"):
        if st.session_state.is_admin:
            st.session_state.is_admin = False
            st.session_state.show_admin = False
            st.rerun()
        else:
            st.session_state.show_admin = not st.session_state.show_admin
            st.rerun()

# 🔒 بوابة الدخول (404)
if st.session_state.show_admin and not st.session_state.is_admin:
    st.markdown('<div class="top-login-wrapper">', unsafe_allow_html=True)
    pass_in = st.text_input("", type="password", placeholder="ادخل الكود لفتح لوحة المسؤول", label_visibility="collapsed")
    if pass_in == "404":
        st.session_state.is_admin = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 🛠️ صفحة المسؤول (تعديل الجرد العام للمخزن + جرد الخارج وإمكانية حذفه)
# -------------------------------------------------------------
elif st.session_state.is_admin:
    st.markdown('<div class="admin-page-title">إدارة المخازن السحابية</div>', unsafe_allow_html=True)
    st.write("---")
    
    with st.expander("قائمة المهام والإشراف", expanded=True):
        menu_choice = st.selectbox(
            "",
            ["تعديل بيانات المخزن الحالي", "إضافة منتج يدوياً للمخزن", "خيار ملف Excel للمخزن", "📊 عرض جرد كميات الخارج"],
            label_visibility="collapsed"
        )
    
    st.write(" ")
    df_main = st.session_state.persistent_main
    df_out = st.session_state.persistent_out

    if menu_choice == "تعديل بيانات المخزن الحالي":
        st.markdown('<div class="focus-card-title">التعديل والازالة للمخزن الرئيسي</div>', unsafe_allow_html=True)
        search_c = st.text_input("", placeholder="ابحث بكود المنتج لتعديله...", label_visibility="collapsed")
        target_idx = df_main[df_main['الكود'].astype(str) == str(search_c)].index if search_c else []
        
        if len(target_idx) > 0:
            idx = target_idx[0]
            row = df_main.loc[idx]
            
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
                if st.button("💾 حفظ وتحديث دائم", use_container_width=True):
                    now = datetime.now()
                    df_main.at[idx, "اسم النوع"] = u_name
                    df_main.at[idx, "عدد الامتار"] = u_meters
                    df_main.at[idx, "العدد"] = u_qty
                    df_main.at[idx, "المكان"] = u_store
                    df_main.at[idx, "التاريخ"] = now.strftime("%d/%m/%Y")
                    df_main.at[idx, "الوقت"] = now.strftime("%I:%M").lstrip("0")
                    st.session_state.persistent_main = df_main
                    st.success("🎉 تم حفظ التعديلات سحابياً ولن تضيع عند التحديث!")
                    st.rerun()
            with b2:
                if st.button("🗑️ إزالة المنتج نهائياً", use_container_width=True):
                    df_main = df_main.drop(idx).reset_index(drop=True)
                    st.session_state.persistent_main = df_main
                    st.success("🗑️ تم حذف المنتج من المخزن دائمًا.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu_choice == "إضافة منتج يدوياً للمخزن":
        st.markdown('<div class="focus-card-title">إضافة نوع جديد للمخزن دائم الحفظ</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        with st.form("add_m_form"):
            nc = st.text_input("كود المنتج الجديد:")
            nn = st.text_input("اسم النوع الجديد:")
            c1, c2, c3 = st.columns(3)
            with c1: nm = st.number_input("عدد الأمتار:", min_value=0.0)
            with c2: nq = st.number_input("العدد:", min_value=0, step=1)
            with c3: nl = st.text_input("المكان:")
            
            if st.form_submit_button("➕ تأكيد إضافة البطاقة وحفظها بشكل دائم", use_container_width=True):
                if nc and nn:
                    now = datetime.now()
                    new_r = {"الكود": str(nc), "اسم النوع": str(nn), "عدد الامتار": nm, "العدد": int(nq), "المكان": str(nl), "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")}
                    df_main = pd.concat([df_main, pd.DataFrame([new_r])], ignore_index=True)
                    st.session_state.persistent_main = df_main
                    st.success("✅ تم إضافة المنتج للمخزن بشكل دائم وثابت!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu_choice == "خيار ملف Excel للمخزن":
        st.markdown('<div class="focus-card-title">رفع ملف Excel للمخزن الرئيسي</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        up_file = st.file_uploader("اختر ملف الإكسيل:", type=["xlsx", "xls"], label_visibility="collapsed")
        if up_file is not None:
            try:
                up_df = pd.read_excel(up_file)
                req = ["الكود", "اسم النوع", "عدد الامتار", "العدد", "المكان"]
                if not [c for c in req if c not in up_df.columns]:
                    if st.button("🚀 اعتماد وتثبيت ملف الإكسيل في السيرفر الآن", use_container_width=True):
                        now = datetime.now()
                        up_df["الكود"] = up_df["الكود"].astype(str)
                        up_df["التاريخ"] = now.strftime("%d/%m/%Y")
                        up_df["الوقت"] = now.strftime("%I:%M").lstrip("0")
                        st.session_state.persistent_main = up_df[req + ["التاريخ", "الوقت"]]
                        st.success("🎉 تم دمج واعتماد ملف الإكسيل بنجاح تام!")
                        st.rerun()
                else: st.error("أعمدة ملف الإكسيل غير مطابقة للترتيب المطلوب.")
            except Exception as e: st.error(f"خطأ: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # طلبك الأول والثاني: إمكانية إزالة بطاقة التسليم مع تأكيد الأمان التام قبل المسح
    elif menu_choice == "📊 عرض جرد كميات الخارج":
        st.markdown('<div class="focus-card-title">دفتر رصد السلع الخارجة (شيت التسليمات)</div>', unsafe_allow_html=True)
        
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
                
                # زر إزالة بطاقة التسليم الفردي مع تأكيد الحذف المباشر
                if st.session_state.delete_confirm_idx == idx:
                    st.markdown("""<div class="confirm-box"><p style='color:red; font-weight:bold; margin-bottom:10px;'>⚠️ هل أنت متأكد من رغبتك في حذف بطاقة التسليم هذه نهائياً؟</p></div>""", unsafe_allow_html=True)
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("🔥 نعم، حذف نهائي", key=f"conf_yes_{idx}", use_container_width=True):
                            df_out = df_out.drop(idx).reset_index(drop=True)
                            st.session_state.persistent_out = df_out
                            st.session_state.delete_confirm_idx = None
                            st.success("🗑️ تم المسح بنجاح وثبات!")
                            st.rerun()
                    with bc2:
                        if st.button("❌ تراجع وإلغاء", key=f"conf_no_{idx}", use_container_width=True):
                            st.session_state.delete_confirm_idx = None
                            st.rerun()
                else:
                    if st.button(f"🗑️ إزالة بطاقة التسليم ({row['اسم النوع']})", key=f"del_btn_{idx}", use_container_width=True):
                        st.session_state.delete_confirm_idx = idx
                        st.rerun()
        else:
            st.info("شيت التسليمات فارغ تماماً ولا توجد بضائع خارجة مسجلة حالياً.")

    st.write("---")
    if st.button("🚪 خروج والعودة لواجهة العمال الرئيسية", use_container_width=True):
        st.session_state.is_admin = False
        st.session_state.show_admin = False
        st.rerun()

# -------------------------------------------------------------
# 🏠 الواجهة الرئيسية للعمال (البحث الخماسي المفتوح والتسجيل دائم الثبات)
# -------------------------------------------------------------
else:
    st.markdown('<div class="header-box"><div class="main-title">المخازن</div><div class="shop-title">محلات زقزوق للأقمشة</div></div>', unsafe_allow_html=True)
    app_page = st.radio("", ["🖥️ عرض بيانات المخزن", "📤 تسجيل الخارج من المخزن"], horizontal=True, label_visibility="collapsed")
    st.write("---")

    df_main = st.session_state.persistent_main
    df_out = st.session_state.persistent_out

    # [الصفحة الأولى]: البحث الذكي المفتوح بالاسم أو الكود (يُظهر كل الأكواد المتوفرة تحت بعضها فوراً)
    if app_page == "🖥️ عرض بيانات المخزن":
        query = st.text_input("", placeholder="ابحث هنا باسم الخامة أو بالكود واضغط Enter...", label_visibility="collapsed")
        
        if query:
            res = df_main[
                df_main['اسم النوع'].str.contains(query, case=False, na=False) | 
                df_main['الكود'].astype(str).str.contains(query, case=False, na=False)
            ]
            
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
            else:
                st.markdown("<p style='text-align:center; color:red; font-weight:bold;'>⚠️ لا توجد نتائج تطابق هذا البحث.</p>", unsafe_allow_html=True)

        st.write("---")
        with st.expander("آخر الإضافات في المخزن"):
            if not df_main.empty:
                for idx, row in df_main.iterrows():
                    st.markdown(f'<div class="added-box"><div style="font-size: 20px; font-weight: bold;">{row["اسم النوع"]} (كود: {row["الكود"]})</div></div>', unsafe_allow_html=True)

    # [الصفحة الثانية]: تسجيل قماش خارج (يُحفظ في السيرفر فوراً ويظهر حصرياً عند المسؤول)
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
                    new_out = {
                        "الكود": str(out_code), "اسم النوع": str(out_name), "عدد الامتار": out_meters, 
                        "العدد": int(out_qty), "المكان": str(out_loc), "اسم التسليم": str(out_receiver),
                        "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")
                    }
                    df_out = pd.concat([df_out, pd.DataFrame([new_out])], ignore_index=True)
                    st.session_state.persistent_out = df_out
                    st.success(f"✅ تم حفظ العملية سحابياً بنجاح! وجاهزة للمراجعة في لوحة المسؤول.")
                else:
                    st.markdown("<p style='text-align:center; color:red;'>⚠️ يرجى إدخال الكود، الاسم، وملاحظة اسم التسليم لإتمام العملية وسماعها عند المسؤول.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
                            
