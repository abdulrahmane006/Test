import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="المخازن - محلات زقزوق", layout="centered")

# 2. تصميم الواجهة بالكامل (الحواف المنحنية، التوسيط الكامل، وتساوي المستطيلات)
st.markdown("""
    <style>
    .stApp { direction: RTL; text-align: right; background-color: #ffffff; color: #000000; }
    
    /* تنسيق الهيدر للواجهة الرئيسية */
    .header-box { text-align: center; margin-top: 5px; margin-bottom: 25px; }
    .main-title { font-size: 38px; font-weight: bold; color: #000000; line-height: 1.0; }
    .shop-title { font-size: 16px; color: #555555; margin-top: 5px; }
    
    /* جعل كل الحواف في الأزرار والخانات والقوائم منحنية وتوسيط النصوص بداخلها */
    input, .stButton>button, div[data-testid="stExpander"], .stSelectbox>div>div { 
        border-radius: 15px !important; 
        text-align: center !important;
    }
    
    /* ضبط خانة البحث الرئيسية لتكون جهة اليسار كما طلبت سابقاً */
    .main-search input { text-align: left !important; direction: ltr !important; }
    
    /* توسيط نصوص المدخلات داخل صفحة المسؤول وتساويها */
    .admin-inputs input { text-align: center !important; }
    
    /* بطاقة النتيجة المنحنية الموحدة الشاملة للمستخدم والمسؤول */
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
    
    /* جدول الأعمدة الموسطة المتساوية */
    .card-columns { display: flex; justify-content: space-around; margin-top: 10px; text-align: center; }
    .card-col { flex: 1; text-align: center; }
    .col-label { font-size: 14px; color: #777777; margin-bottom: 4px; }
    .col-value { font-size: 18px; font-weight: bold; color: #000000; }
    
    /* تخصيص قوائم الاختيار والتبويبات لتظهر في المنتصف تماماً */
    .stExpanderSummary p { font-size: 22px !important; font-weight: bold !important; text-align: center !important; width: 100%; }
    .added-box {
        border: 1px solid #999999;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #ffffff;
        text-align: center;
    }
    
    /* تخصيص صندوق الكود السري الموسط النظيف */
    .login-container {
        border: 2px solid #000000;
        border-radius: 20px;
        padding: 35px;
        max-width: 350px;
        margin: 100px auto;
        text-align: center;
    }
    
    /* تنسيقات عناوين صفحة المسؤول الموسطة */
    .admin-page-title { font-size: 26px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 20px; }
    .admin-section-title { font-size: 22px; font-weight: bold; color: #000000; text-align: center; margin-bottom: 15px; }
    
    /* محاذاة أرقام مدخلات النماذج لتكون موسطة */
    div[data-testid="stMarkdownContainer"] > p { text-align: center !important; }
    label { width: 100%; text-align: center !important; display: block !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# 3. قاعدة البيانات الافتراضية للبرنامج
if 'products_db' not in st.session_state:
    st.session_state.products_db = pd.DataFrame([
        {"الكود": "101", "اسم النوع": "دم غزال", "اللون": "احمر", "المخزن": "العشة", "العدد المتوفر": 3, "التاريخ": "13/6/2026", "الوقت": "3:39"}
    ])

if 'show_admin_flow' not in st.session_state:
    st.session_state.show_admin_flow = False
if 'is_admin_logged' not in st.session_state:
    st.session_state.is_admin_logged = False

# 4. الترس أعلى اليمين للتحويل بين الصفحات وقفل الجلسة بأمان
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
# 🔒 بـوابـة المسؤول (المستطيل الموسط النظيف بكلمة ادخل الكود بالداخل)
# -------------------------------------------------------------
if st.session_state.show_admin_flow and not st.session_state.is_admin_logged:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    pass_in = st.text_input("", type="password", placeholder="ادخل الكود", label_visibility="collapsed")
    if pass_in == "404":
        st.session_state.is_admin_logged = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 🛠️ صـفـحـة الـمـسـؤول الـمـطـورة (عند كـتـابـة 404 بنجاح)
# -------------------------------------------------------------
elif st.session_state.is_admin_logged:
    st.markdown('<div class="admin-page-title">لوحة تحكم محلات زقزوق</div>', unsafe_allow_html=True)
    st.write("---")
    
    # قائمة المهام الموسطة المنحنية الشاملة لخياراتك الثلاثة
    with st.expander("📋 قائمة المهام"):
        menu_choice = st.selectbox(
            "",
            ["تعديل البيانات الحالية", "إضافة منتج يدوياً", "خيار ملف Excel"],
            label_visibility="collapsed"
        )
    
    st.write(" ")

    # الخانة الأولى: تعديل البيانات الحالية (البحث بالكود لتعديل أو إزالة منتج مع التأكيد)
    if menu_choice == "تعديل البيانات الحالية":
        st.markdown('<div class="admin-section-title">البحث عن توب وتعديله أو إزالته</div>', unsafe_allow_html=True)
        
        # صندوق البحث الموسط المخصص للمسؤول
        search_code = st.text_input("", placeholder="اكتب كود المنتج واضغط إدخال للبحث...", label_visibility="collapsed")
        
        if search_code:
            df = st.session_state.products_db
            # البحث المطابق تماماً للكود
            product_idx = df[df['الكود'].astype(str) == str(search_code)].index
            
            if not product_idx.empty:
                idx = product_idx[0]
                row = df.loc[idx]
                
                # عرض بطاقة التعديل المنحنية الموسطة المتساوية بالكامل
                st.markdown('<div class="unified-card admin-inputs">', unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:24px; font-weight:bold; margin-bottom:5px;'>{row['اسم النوع']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:16px; color:#666666; margin-bottom:15px;'>كود المنتج المختار: {row['الكود']}</div>", unsafe_allow_html=True)
                
                # الخانات المتساوية المتناسقة لتعديل كل جزئية يدوياً
                c1, c2, c3 = st.columns(3)
                with c1: u_color = st.text_input("اللون", value=row["اللون"], key=f"edit_c_{idx}")
                with c2: u_qty = st.number_input("العدد المتوفر", value=int(row["العدد المتوفر"]), min_value=0, step=1, key=f"edit_q_{idx}")
                with c3: u_store = st.text_input("المكان", value=row["المخزن"], key=f"edit_l_{idx}")
                
                st.write(" ")
                
                # الأزرار في المنتصف تماماً وبشكل متناسق ومساواة كاملة
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    save_btn = st.button("💾 حفظ التعديلات وتحديث الوقت", use_container_width=True)
                with b_col2:
                    delete_btn = st.button("🗑️ إزالة هذا المنتج من المخزن", use_container_width=True, type="secondary")
                
                # تنفيذ الحفظ وتحديث الوقت تلقائياً عند تغيير البيانات فقط
                if save_btn:
                    now = datetime.now()
                    if not (row["اللون"] == u_color and row["العدد المتوفر"] == u_qty and row["المخزن"] == u_store):
                        st.session_state.products_db.at[idx, "اللون"] = u_color
                        st.session_state.products_db.at[idx, "العدد المتوفر"] = u_qty
                        st.session_state.products_db.at[idx, "المخزن"] = u_store
                        st.session_state.products_db.at[idx, "التاريخ"] = now.strftime("%d/%m/%Y")
                        st.session_state.products_db.at[idx, "الوقت"] = now.strftime("%I:%M").lstrip("0")
                        st.success("🎉 تم حفظ التعديلات الجديدة وتحديث التوقيت بنجاح!")
                    else:
                        st.info("لم تقم بتغيير أي بيانات لحفظها.")
                    st.rerun()
                
                # تفعيل آلية التأكيد قبل الإزالة لمنع الأخطاء العمالية
                if delete_btn or st.session_state.get(f"confirm_del_{idx}", False):
                    st.session_state[f"confirm_del_{idx}"] = True
                    st.markdown("<p style='color:red; font-weight:bold; text-align:center;'>⚠️ هل أنت متأكد تماماً من إزالة هذا المنتج نهائياً؟</p>", unsafe_allow_html=True)
                    
                    del_c1, del_c2 = st.columns(2)
                    with del_c1:
                        if st.button("✅ نعم، تأكيد الحذف النهائي", use_container_width=True, key=f"yes_del_{idx}"):
                            st.session_state.products_db = st.session_state.products_db.drop(idx).reset_index(drop=True)
                            st.session_state[f"confirm_del_{idx}"] = False
                            st.success("🗑️ تم مسح المنتج وإزالته تماماً من قاعدة البيانات.")
                            st.rerun()
                    with del_c2:
                        if st.button("❌ تراجع وإلغاء", use_container_width=True, key=f"no_del_{idx}"):
                            st.session_state[f"confirm_del_{idx}"] = False
                            st.rerun()
                            
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='text-align:center; color:red; font-weight:bold;'>⚠️ لا يوجد منتج مسجل في النظام بهذا الكود.</p>", unsafe_allow_html=True)

    # الخانة الثانية: إضافة منتج يدوياً في بطاقة فارغة موسطة ومتساوية الخانات
    elif menu_choice == "إضافة منتج يدوياً":
        st.markdown('<div class="admin-section-title">إضافة توب جديد للمخزن</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card admin-inputs">', unsafe_allow_html=True)
        with st.form("add_form_admin", clear_on_submit=True):
            nc = st.text_input("كود المنتج الجديد:")
            nn = st.text_input("اسم النوع الجديد:")
            
            c1, c2, c3 = st.columns(3)
            with c1: n_color = st.text_input("اللون:")
            with c2: n_qty = st.number_input("العدد المتوفر:", min_value=0, step=1)
            with c3: n_store = st.text_input("المكان (المخزن):")
            
            st.write(" ")
            if st.form_submit_button("➕ تأكيد إضافة البطاقة وحفظها", use_container_width=True):
                if nc and nn:
                    now = datetime.now()
                    new_row = {
                        "الكود": str(nc), "اسم النوع": str(nn), "اللون": str(n_color), "المخزن": str(n_store), 
                        "العدد المتوفر": int(n_qty), "التاريخ": now.strftime("%d/%m/%Y"), "الوقت": now.strftime("%I:%M").lstrip("0")
                    }
                    st.session_state.products_db = pd.concat([st.session_state.products_db, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("✅ تم إضافة التوب الجديد بنجاح وجاهز للعرض بالرئيسية!")
                    st.rerun()
                else:
                    st.error("⚠️ يرجى تعبئة خانتي الكود واسم النوع أولاً لإتمام الإضافة.")
        st.markdown('</div>', unsafe_allow_html=True)

    # الخانة الثالثة: خيار ملف Excel وتفريغه بالكامل في المخازن
    elif menu_choice == "خيار ملف Excel":
        st.markdown('<div class="admin-section-title">رفع وجلب ملف Excel بالكامل للمخزن</div>', unsafe_allow_html=True)
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        st.write("الأعمدة المطلوبة في الملف: `الكود` | `اسم النوع` | `اللون` | `المخزن` | `العدد المتوفر`")
        st.write(" ")
        up_file = st.file_uploader("اختر ملف الإكسيل المطلوب رفعه:", type=["xlsx", "xls"], label_visibility="collapsed")
        
        if up_file is not None:
            try:
                up_df = pd.read_excel(up_file)
                req = ["الكود", "اسم النوع", "اللون", "المخزن", "العدد المتوفر"]
                if not [c for c in req if c not in up_df.columns]:
                    if st.button("🚀 تفريغ واعتماد ملف الإكسيل وتحويله لبطاقات متتالية", use_container_width=True):
                        now = datetime.now()
                        up_df["الكود"] = up_df["الكود"].astype(str)
                        up_df["اسم النوع"] = up_df["اسم النوع"].astype(str)
                        up_df["اللون"] = up_df["اللون"].fillna("-").astype(str)
                        up_df["المخزن"] = up_df["المخزن"].fillna("-").astype(str)
                        up_df["العدد المتوفر"] = up_df["العدد المتوفر"].fillna(0).astype(int)
                        up_df["التاريخ"] = now.strftime("%d/%m/%Y")
                        up_df["الوقت"] = now.strftime("%I:%M").lstrip("0")
                        
                        st.session_state.products_db = up_df[req + ["التاريخ", "الوقت"]]
                        st.success("🎉 ممتاز! تم تفريغ ملف الإكسيل كاملاً وتحويل البيانات لبطاقات متناسقة!")
                        st.rerun()
                else: 
                    st.error("⚠️ تأكد من كتابة أسماء الأعمدة في الإكسيل بشكل مطابق للتعليمات.")
            except Exception as e: 
                st.error(f"❌ حدث خطأ أثناء قراءة الملف: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("---")
    if st.button("🚪 خروج والعودة لواجهة العمال الرئيسية", use_container_width=True):
        st.session_state.is_admin_logged = False
        st.session_state.show_admin_flow = False
        st.rerun()

# -------------------------------------------------------------
# 🏠 الـواجـهـة الـرئـيـسـيـة للمحل (تظهر للعمال و المرور بشكل طبيعي)
# -------------------------------------------------------------
else:
    st.markdown("""
        <div class="header-box">
            <div class="main-title">المخازن</div>
            <div class="shop-title">محلات زقزوق للأقمشة</div>
        </div>
    """, unsafe_allow_html=True)

    st.write(" ")
    # خانة البحث الرئيسية الموجهة لليسار بنص شفاف عربي
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
            st.markdown("<p style='text-align:center; color:red; font-weight:bold;'>⚠️ لا توجد نتائج تطابق هذا البحث.</p>", unsafe_allow_html=True)

    st.write("---")

    # تبويب آخر الإضافات العريض والموسط والخط العريض تماماً وبدون إيموجيز
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
            
