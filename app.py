import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="المخازن", page_icon="📦", layout="centered")

# تطبيق التصميم الأسود البسيط وتنسيق محاذاة العناصر (RTL) في المنتصف
st.markdown("""
    <style>
    /* جعل الخلفية بيضاء والنصوص سوداء بالكامل */
    .stApp {
        direction: RTL;
        text-align: right;
        background-color: #ffffff;
        color: #000000;
    }
    /* جعل العناوين باللون الأسود وفي المنتصف */
    .main-title {
        text-align: center;
        color: #000000;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    /* تنسيق أزرار التبويبات وخانات الإدخال لتكون باللون الأسود والرمادي الداكن */
    .stButton>button {
        color: #ffffff;
        background-color: #000000;
        border-radius: 4px;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #000000;
        border-radius: 4px;
        background-color: #fafafa;
    }
    </style>
""", unsafe_allow_html=True)

# 1. قاعدة البيانات الافتراضية - تم إصلاح الأقواس هنا بالكامل
if 'products_db' not in st.session_state:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.products_db = pd.DataFrame([
        {"الكود": "101", "اسم النوع": "توب قطن حريمي", "اللون": "أسود", "المخزن": "مخزن أ", "العدد المتوفر": 25, "تاريخ آخر تعديل": current_time},
        {"الكود": "102", "اسم النوع": "توب صوف رجالي", "اللون": "أزرق", "المخزن": "مخزن ب", "العدد المتوفر": 14, "تاريخ آخر تعديل": current_time},
        {"الكود": "125", "اسم النوع": "دم غزال", "اللون": "أحمر", "المخزن": "المخزن الرئيسي", "العدد المتوفر": 80, "تاريخ آخر تعديل": current_time}
    ])

# كود المسؤول السري (404)
ADMIN_PASSWORD = "404"

# وضع أيقونة الترس فوق على اليسار للمسؤول باستخدام أعمدة رشيقة
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    admin_clicked = st.button("⚙️", help="بوابة المسؤول")
    if admin_clicked:
        st.session_state.show_admin_login = not st.session_state.get('show_admin_login', False)

# تفعيل حالة إظهار خانة الكود السري عند الضغط على الترس
if st.session_state.get('show_admin_login', False):
    password_input = st.text_input("أدخل كود المسؤول السري:", type="password")
else:
    password_input = ""

# العنوان الرئيسي في المنتصف تماماً وبدون أي صناديق
st.markdown('<div class="main-title">المخازن</div>', unsafe_allow_html=True)
st.write(" ")

# -------------------------------------------------------------
# 📋 زر وقائمة "آخر التعديلات" المنبثقة
# -------------------------------------------------------------
with st.expander("📊 آخر التعديلات"):
    if not st.session_state.products_db.empty:
        db_copy = st.session_state.products_db.copy()
        # صياغة النص المطلوب: دم غزال (125) ... تاريخ التعديل
        db_copy['display_text'] = db_copy.apply(
            lambda r: f"{r['اسم النوع']} ({r['الكود']}) ... آخر تعديل: {r['تاريخ آخر تعديل']}", axis=1
        )
        st.selectbox("استعراض القائمة المتوفرة حالياً:", options=db_copy['display_text'], label_visibility="collapsed")
    else:
        st.write("لا توجد منتجات مسجلة.")

st.write("---")

# -------------------------------------------------------------
# 🔍 خانة البحث النظيفة في منتصف الصفحة والنتائج التلقائية
# -------------------------------------------------------------
search_query = st.text_input("", placeholder="ابحث باسم النوع أو كود المنتج...", label_visibility="collapsed")

if search_query:
    df = st.session_state.products_db
    filtered_df = df[
        df['اسم النوع'].str.contains(search_query, case=False, na=False) | 
        df['الكود'].astype(str).str.contains(search_query, case=False, na=False)
    ]
    
    if not filtered_df.empty:
        # عرض التفاصيل تلقائياً ومنسدلة بشكل فوري ومريح
        for index, row in filtered_df.iterrows():
            with st.container(border=True):
                st.markdown(f"### 📌 {row['اسم النوع']} ({row['الكود']})")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="العدد المتوفر", value=f"{row['العدد المتوفر']} قطعة")
                with col2:
                    st.text_input(label="اللون المتاح", value=row['اللون'], disabled=True, key=f"src_col_{index}")
                with col3:
                    st.text_input(label="مكان التخزين", value=row['المخزن'], disabled=True, key=f"src_loc_{index}")
                st.caption(f"🕒 تاريخ التوثيق: {row['تاريخ آخر تعديل']}")
    else:
        st.warning("⚠️ لا توجد نتائج تطابق بحثك.")

st.write("---")

# -------------------------------------------------------------
# 🛠️ واجهة المسؤول عند كتابة كود 404
# -------------------------------------------------------------
if password_input == ADMIN_PASSWORD:
    st.markdown("### 🛠️ لوحة تحكم المسؤول")
    
    admin_tabs = st.tabs(["✏️ تعديل وجرد البيانات", "➕ إضافة منتج منفرد", "📂 رفع ملف Excel", "⚙️ إعادة ترتيب وتسمية البيانات"])
    
    # 1. التعديل المباشر
    with admin_tabs[0]:
        st.subheader("تعديل فوري على الجدول")
        edited_df = st.data_editor(st.session_state.products_db, use_container_width=True, num_rows="dynamic")
        if st.button("💾 حفظ التعديلات وتحديث التواريخ"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            if len(edited_df) == len(st.session_state.products_db):
                for i in range(len(edited_df)):
                    old_r = st.session_state.products_db.iloc[i].drop("تاريخ آخر تعديل", errors='ignore')
                    new_r = edited_df.iloc[i].drop("تاريخ آخر تعديل", errors='ignore')
                    if not old_r.equals(new_r):
                        edited_df.at[i, "تاريخ آخر تعديل"] = current_time
            else:
                edited_df["تاريخ آخر تعديل"] = edited_df["تاريخ آخر تعديل"].fillna(current_time)
            st.session_state.products_db = edited_df
            st.success("✅ تم تحديث المخازن بنجاح!")
            st.rerun()

    # 2. إضافة منتج منفرد
    with admin_tabs[1]:
        st.subheader("إدخال صنف جديد")
        with st.form("quick_add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                new_code = st.text_input("كود المنتج:")
                new_name = st.text_input("اسم النوع:")
                new_color = st.text_input("اللون:")
            with c2:
                new_store = st.text_input("المخزن:")
                new_qty = st.number_input("العدد المتوفر:", min_value=0, step=1)
            
            if st.form_submit_button("➕ تأكيد الحفظ للمخزن"):
                if new_code and new_name:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    new_row = {"الكود": str(new_code), "اسم النوع": str(new_name), "اللون": str(new_color), "المخزن": str(new_store), "العدد المتوفر": int(new_qty), "تاريخ آخر تعديل": current_time}
                    st.session_state.products_db = pd.concat([st.session_state.products_db, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("✅ تم الحفظ.")
                    st.rerun()

    # 3. رفع ملف إكسيل كامل وتنظيمه تلقائياً
    with admin_tabs[2]:
        st.subheader("📂 رفع وترتيب ملف Excel تلقائياً")
        st.write("الأعمدة المطلوبة في ملف الإكسيل الخاص بك: `الكود` | `اسم النوع` | `اللون` | `المخزن` | `العدد المتوفر`")
        uploaded_file = st.file_uploader("اختر ملف الإكسيل من جهازك:", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_excel(uploaded_file)
                required_cols = ["الكود", "اسم النوع", "اللون", "المخزن", "العدد المتوفر"]
                missing_cols = [col for col in required_cols if col not in uploaded_df.columns]
                
                if not missing_cols:
                    if st.button("🚀 اعتماد وتنظيم الإكسيل فوراً"):
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                        uploaded_df["الكود"] = uploaded_df["الكود"].astype(str)
                        uploaded_df["اسم النوع"] = uploaded_df["اسم النوع"].astype(str)
                        uploaded_df["اللون"] = uploaded_df["اللون"].fillna("-").astype(str)
                        uploaded_df["المخزن"] = uploaded_df["المخزن"].fillna("-").astype(str)
                        uploaded_df["العدد المتوفر"] = uploaded_df["العدد المتوفر"].fillna(0).astype(int)
                        uploaded_df["تاريخ آخر تعديل"] = current_time
                        
                        st.session_state.products_db = uploaded_df[required_cols + ["تاريخ آخر تعديل"]]
                        st.success("🎉 ممتاز! تم سحب البيانات وتنظيمها بالكامل وتوثيق تاريخ اليوم.")
                        st.rerun()
                else:
                    st.error(f"الملف يفتقد لبعض الأعمدة: {missing_cols}")
            except Exception as e:
                st.error(f"خطأ في قراءة ملف الإكسيل: {e}")

    # 4. التحكم في ترتيب وتسمية الأعمدة الظاهرة
    with admin_tabs[3]:
        st.subheader("⚙️ التحكم في ترتيب وتسمية البيانات")
        st.write("يمكنك إعادة ترتيب صفوف البيانات الحالية لتظهر بالترتيب الذي تفضله:")
        
        if not st.session_state.products_db.empty:
            sort_by = st.selectbox("ترتيب عرض المنتجات تلقائياً حسب:", ["اسم النوع", "الكود", "العدد المتوفر"])
            ascending_choice = st.radio("اتجاه الترتيب:", ["تصاعدي", "تنازلي"])
            
            if st.button("🔄 تطبيق الترتيب الجديد للمخزن"):
                is_asc = True if ascending_choice == "تصاعدي" else False
                st.session_state.products_db = st.session_state.products_db.sort_values(by=sort_by, ascending=is_asc).reset_index(drop=True)
                st.success("✅ تم إعادة ترتيب وتنسيق ظهور البيانات بنجاح!")
                st.rerun()
else:
    if password_input:
        st.error("الكود السري غير صحيح!")
        
