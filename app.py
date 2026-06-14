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
st.markdown('<div class="main-title">المخاز
    </style>
""", unsafe_allow_html=True)

# 1. قاعدة البيانات الافتراضية وهيكلة الأعمدة
if 'products_db' not in st.session_state:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.products_db = pd.DataFrame([
        {"الكود": "101", "اسم النوع": "توب قطن حريمي", "اللون": "أسود", "المخزن": "مخزن أ", "العدد المتوفر": 25, "تاريخ آخر تعديل": current_time},
        {"الكود": "102", "اسم النوع": "توب صوف رجالي", "اللون": "أزرق", "المخزن": "مخزن ب", "العدد المتوفر": 14, "تاريخ آخر تعديل": current_time},
        {"الكود": "125", "اسم النوع": "دم غزال", "اللون": "أحمر", "المخزن": "المخزن الرئيسي", "العدد المتوفر": 80, "تاريخ آخر تعديل": current_time},
    ])

# كود المسؤول الجديد الذي طلبته
ADMIN_PASSWORD = "404"

# وضع أيقونة الترس فوق على اليسار للمسؤول باستخدام أعمدة رشيقة
top_col1, top_col2 = st.columns([9, 1])
with top_col2:
    # زر الترس الصغير لتسجيل الدخول كمسؤول
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
    # تصفية البحث لمنع حدوث أي خطأ NameError
    filtered_df = df[
        df['اسم النوع'].str.contains(search_query, case=False, na=False) | 
        df['الكود'].astype(str).str.contains(search_query, case=False, na=False)
    ]
    
    if not filtered_df.empty:
        # عرض التفاصيل تلقائياً ومنسدلة بشكل فوري ومريح للمرور
        for index, row in filtered_df.iterrows():
            with st.container(border=True):
                st.markdown(f"### 📌 {row['اسم النوع']} ({row['الكود']})")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="العدد المتوفر", value=f"{row['العدد المتوفر']} قطة")
                with col2:
                    st.text_input(label="اللون المتاح", value=row['اللون'], disabled=True, key=f"src_col_{index}")
                with col3:
                    st.text_input(label="مكان التخزين", value=row['المخزن'], disabled=True, key=f"src_loc_{index}")
                st.caption(f"🕒 تاريخ التوثيق: {row['تاريخ آخر تعديل']}")
    else:
        st.warning("⚠️ لا توجد نتائج تطابق بحثك.")

st.write("---")

# -------------------------------------------------------------
# 🛠️ واجهة المسؤول عند كتابة كود 404 (إخفاء وإظهار كامل وتعديل الترتيب)
# -------------------------------------------------------------
if password_input == ADMIN_PASSWORD:
    st.black_header = st.markdown("### 🛠️ لوحة تحكم المسؤول")
    
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

    # 4. تلبية طلب التحكم في تسمية وترتيب الأعمدة الظاهرة للمرور
    with admin_tabs[3]:
        st.subheader("⚙️ التحكم في ترتيب وتسمية البيانات")
        st.write("يمكنك إعادة ترتيب صفوف البيانات الحالية للأعلى أو الأسفل لتظهر للمرور بالترتيب الذي تفضله:")
        
        if not st.session_state.products_db.empty:
            # ترتيب حسب اختيار المسؤول لاسم النوع أو الكود ليكون العرض منضبطاً
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
    ])

# الكود السري الخاص بالمسؤول
ADMIN_PASSWORD = "admin"

# العنوان الرئيسي المبسط
st.title("📦 المخازن")
st.write("---")

# -------------------------------------------------------------
# 📑 أولاً: القائمة المنسدلة لجميع الأنواع والأكواد والتواريخ
# -------------------------------------------------------------
st.subheader("📋 استعراض الأنواع المسجلة تواريخها")

if not st.session_state.products_db.empty:
    # تجهيز النص المكتوب داخل القائمة (النوع - الكود - تاريخ التعديل)
    db_copy = st.session_state.products_db.copy()
    db_copy['display_text'] = db_copy.apply(
        lambda r: f"النوع: {r['اسم النوع']} | الكود: {r['الكود']} | (آخر تعديل: {r['تاريخ آخر تعديل']})", axis=1
    )
    
    # القائمة المنسدلة للمشاهدة السريعة
    st.selectbox("اضغط هنا لرؤية قائمة بجميع الأنواع المتوفرة وتواريخها:", options=db_copy['display_text'])
else:
    st.info("المخزن فارغ حالياً.")

st.write("---")

# -------------------------------------------------------------
# 🔍 ثانياً: زر البحث الذكي والنتائج الانسدالية
# -------------------------------------------------------------
st.subheader("🔍 ابحث عن منتج")

search_query = st.text_input("أدخل اسم النوع أو كود المنتج لبدء الجرد والبحث:", placeholder="اكتب هنا...")

if search_query:
    df = st.session_state.products_db
    filtered_df = df[
        df['اسم النوع'].str.contains(search_query, case=False, na=False) | 
        df['الكود'].astype(str).str.contains(search_query, case=False, na=False)
    ]
    
    if not filtered_df.empty:
        st.write(f"🔹 تم العثور على ({len(filtered_df)}) منتج. اضغط على المنتج لعرض تفاصيله ومكانه:")
        
        # عرض النتائج بطريقة انسدالية (Expander) لكل منتج على حدة
        for index, row in filtered_df.iterrows():
            with st.expander(f"📌 {row['اسم النوع']} (كود: {row['الكود']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="العدد المتوفر", value=f"{row['العدد المتوفر']} توب")
                with col2:
                    st.text_input(label="اللون", value=row['اللون'], disabled=True, key=f"col_{index}")
                with col3:
                    st.text_input(label="مكان التخزين", value=row['المخزن'], disabled=True, key=f"loc_{index}")
                
                st.caption(f"🕒 تاريخ وثيقة التعديل: {row['تاريخ آخر تعديل']}")
    else:
        st.warning("⚠️ عذراً، لا يوجد منتج يطابق هذا الاسم أو الكود.")
else:
    st.caption("💡 اكتب الكود أو الاسم بالأعلى لتظهر لك تفاصيل الألوان والكميات والمخازن فوراً.")

st.write("---")

# -------------------------------------------------------------
# 🔐 ثالثاً: واجهة المسؤول المنضبطة (أسفل الصفحة)
# -------------------------------------------------------------
st.write(" ")
st.write(" ")

with st.container(border=True):
    st.markdown("### 🔐 بوابة إدارة المخزن (خاص بالمسؤول)")
    password_input = st.text_input("أدخل الكود السري لفتح صلاحيات التعديل والرفع:", type="password")

if password_input == ADMIN_PASSWORD:
    st.success("🔓 وضع المسؤول نشط الآن. يمكنك إجراء أي تعديلات بالأسفل:")
    
    admin_tabs = st.tabs(["✏️ تعديل الكميات والبيانات", "➕ إضافة منتج منفرد", "📂 رفع ملف إكسيل كامل", "❌ حذف منتج"])
    
    # 1. التعديل المباشر
    with admin_tabs[0]:
        st.subheader("تعديل وجرد فوري")
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
            st.success("✅ تم الحفظ بنجاح!")
            st.rerun()

    # 2. إضافة منتج منفرد
    with admin_tabs[1]:
        st.subheader("إضافة توب جديد للمخازن")
        with st.form("add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                new_code = st.text_input("كود المنتج:")
                new_name = st.text_input("اسم النوع:")
                new_color = st.text_input("اللون:")
            with c2:
                new_store = st.text_input("المخزن:")
                new_qty = st.number_input("الكمية المتوفرة:", min_value=0, step=1)
            
            if st.form_submit_button("➕ تأكيد الإضافة للمخزن"):
                if new_code and new_name:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    new_row = {"الكود": str(new_code), "اسم النوع": str(new_name), "اللون": str(new_color), "المخزن": str(new_store), "العدد المتوفر": int(new_qty), "تاريخ آخر تعديل": current_time}
                    st.session_state.products_db = pd.concat([st.session_state.products_db, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("✅ تم إضافة المنتج الجديد!")
                    st.rerun()
                else:
                    st.error("يرجى كتابة الكود والاسم")

    # 3. رفع ملف إكسيل كامل
    with admin_tabs[2]:
        st.subheader("📂 تنظيم ورفع البيانات عبر ملف Excel")
        st.write("الأعمدة المطلوبة في الإكسيل بالترتيب: `الكود` | `اسم النوع` | `اللون` | `المخزن` | `العدد المتوفر`")
        uploaded_file = st.file_uploader("اختر الملف المرفوع:", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_excel(uploaded_file)
                required_cols = ["الكود", "اسم النوع", "اللون", "المخزن", "العدد المتوفر"]
                missing_cols = [col for col in required_cols if col not in uploaded_df.columns]
                
                if not missing_cols:
                    if st.button("🚀 استيراد وتنظيم البيانات تلقائياً"):
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                        uploaded_df["الكود"] = uploaded_df["الكود"].astype(str)
                        uploaded_df["اسم النوع"] = uploaded_df["اسم النوع"].astype(str)
                        uploaded_df["اللون"] = uploaded_df["اللون"].fillna("-").astype(str)
                        uploaded_df["المخزن"] = uploaded_df["المخزن"].fillna("-").astype(str)
                        uploaded_df["العدد المتوفر"] = uploaded_df["العدد المتوفر"].fillna(0).astype(int)
                        uploaded_df["تاريخ آخر تعديل"] = current_time
                        
                        st.session_state.products_db = uploaded_df[required_cols + ["تاريخ آخر تعديل"]]
                        st.success("🎉 تم تنظيم ورفع كافة المنتجات وتحديث تواريخها تلقائياً!")
                        st.rerun()
                else:
                    st.error(f"الملف يفتقد أعمدة أساسية: {missing_cols}")
            except Exception as e:
                st.error(f"خطأ في الملف: {e}")

    # 4. حذف منتج
    with admin_tabs[3]:
        st.subheader("🗑️ إزالة نوع من المخازن")
        product_to_delete = st.selectbox("اختر الصنف المراد حذفه:", options=st.session_state.products_db['اسم النوع'].unique() if not st.session_state.products_db.empty else ["فارغ"])
        if st.button("🗑️ حذف نهائي") and not st.session_state.products_db.empty:
            st.session_state.products_db = st.session_state.products_db[st.session_state.products_db['اسم النوع'] != product_to_delete]
            st.success("تم الحذف.")
            st.rerun()
else:
    if password_input:
        st.error("الكود السري غير صحيح. واجهة الإدارة مقفلة.")
        filtered_df = df

    if not filtered_df.empty:
        st.subheader("📋 نتائج البحث المتوفرة:")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ لا توجد نتائج تطابق هذا البحث حالياً.")

with main_tab2:
    st.header("📋 جرد كافة المنتجات الحالية")
    st.write("الجدول أدناه يوضح جميع المنتجات المسجلة بالمحل وتواريخ تحديثها بشكل لحظي:")
    
    if not st.session_state.products_db.empty:
        st.dataframe(st.session_state.products_db, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ قاعدة البيانات فارغة تماماً حالياً. يرجى من المسؤول رفع أو إضافة منتجات.")

st.write("---")

# -------------------------------------------------------------
# الجزء الثاني: واجهة المسؤول المحمية (تحديث، إضافة، رفع ملفات إكسيل)
# -------------------------------------------------------------
with st.sidebar:
    st.header("🔐 صلاحيات المسؤول")
    password_input = st.text_input("أدخل الكود السري لتعديل البيانات والرفع:", type="password")

if password_input == ADMIN_PASSWORD:
    st.success("🔓 تم الدخول كمسؤول بنجاح!")
    
    # تبويبات الإدارة
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
        "✏️ تعديل سريع وجرد وتواريخ", 
        "➕ إضافة منتج منفرد", 
        "📂 رفع ملف إكسيل كامل",
        "❌ حذف منتج"
    ])
    
    # التبويب الأول للمسؤول: التعديل المباشر وتحديث الوقت تلقائياً
    with admin_tab1:
        st.subheader("تعديل مباشر على جدول المنتجات")
        st.write("يمكنك تعديل أي خانة مباشرة، وسيتم تحديث تاريخ التعديل للمنتج فور الحفظ.")
        
        # محرر بيانات متطور وديناميكي
        edited_df = st.data_editor(st.session_state.products_db, use_container_width=True, num_rows="dynamic")
        
        if st.button("💾 حفظ التعديلات الكلية وتحديث التواريخ"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # مقارنة بسيطة لتحديث التواريخ للأسطر المعدلة فقط
            if len(edited_df) == len(st.session_state.products_db):
                for index in range(len(edited_df)):
                    old_row = st.session_state.products_db.iloc[index].drop("تاريخ آخر تعديل", errors='ignore')
                    new_row = edited_df.iloc[index].drop("تاريخ آخر تعديل", errors='ignore')
                    if not old_row.equals(new_row):
                        edited_df.at[index, "تاريخ آخر تعديل"] = current_time
            else:
                if "تاريخ آخر تعديل" in edited_df.columns:
                    edited_df["تاريخ آخر تعديل"] = edited_df["تاريخ آخر تعديل"].fillna(current_time)
                else:
                    edited_df["تاريخ آخر تعديل"] = current_time
                    
            st.session_state.products_db = edited_df
            st.success("✅ تم حفظ جميع التعديلات وتوثيق التواريخ الجديدة بنجاح!")
            st.rerun()

    # التبويب الثاني للمسؤول: إضافة منتج فردي
    with admin_tab2:
        st.subheader("إضافة منتج جديد بشكل منفرد")
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_code = st.text_input("كود المنتج الجديد:")
                new_name = st.text_input("اسم النوع:")
            with col2:
                new_color = st.text_input("اللون:")
                new_store = st.text_input("المخزن / رف التخزين:")
            with col3:
                new_qty = st.number_input("العدد المتوفر الحالي:", min_value=0, step=1)
            
            submit_btn = st.st.form_submit_button("➕ إضافة المنتج إلى النظام")
            
            if submit_btn:
                if new_code and new_name:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                    new_row = {
                        "الكود": str(new_code), 
                        "اسم النوع": str(new_name), 
                        "اللون": str(new_color), 
                        "المخزن": str(new_store), 
                        "العدد المتوفر": int(new_qty),
                        "تاريخ آخر تعديل": current_time
                    }
                    st.session_state.products_db = pd.concat([st.session_state.products_db, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"✅ تم إضافة المنتج '{new_name}' وتوثيق التاريخ بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ عذراً، يجب ملء خانة 'الكود' و 'اسم النوع' على الأقل.")

    # التبويب الثالث للمسؤول: رفع ملف إكسيل كامل لتحديث البيانات تلقائياً
    with admin_tab3:
        st.subheader("📂 استيراد ورفع البيانات من ملف Excel")
        st.write("ارفع ملف إكسيل يحتوي على الأعمدة التالية ليقوم الموقع بتنظيمها تلقائياً بالكامل:")
        st.markdown("**الأعمدة المطلوبة داخل ملف الإكسيل ليعمل بكفاءة:** `الكود` | `اسم النوع` | `اللون` | `المخزن` | `العدد المتوفر`")
        
        uploaded_file = st.file_uploader("اختر ملف إكسيل (.xlsx أو .xls):", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_excel(uploaded_file)
                required_cols = ["الكود", "اسم النوع", "اللون", "المخزن", "العدد المتوفر"]
                missing_cols = [col for col in required_cols if col not in uploaded_df.columns]
                
                if not missing_cols:
                    if st.button("🚀 اعتماد الملف المرفوع وتحديث قاعدة البيانات"):
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                        
                        # تنظيف البيانات وتثبيت التاريخ تلقائياً لكل البيانات المرفوعة
                        uploaded_df["الكود"] = uploaded_df["الكود"].astype(str)
                        uploaded_df["اسم النوع"] = uploaded_df["اسم النوع"].astype(str)
                        uploaded_df["اللون"] = uploaded_df["اللون"].fillna("-").astype(str)
                        uploaded_df["المخزن"] = uploaded_df["المخزن"].fillna("-").astype(str)
                        uploaded_df["العدد المتوفر"] = uploaded_df["العدد المتوفر"].fillna(0).astype(int)
                        uploaded_df["تاريخ آخر تعديل"] = current_time
                        
                        st.session_state.products_db = uploaded_df[required_cols + ["تاريخ آخر تعديل"]]
                        st.success("🎉 مبروك! تم رفع ملف الإكسيل بنجاح، وقام الموقع بتنظيم كافة المنتجات وتوثيق تاريخ اليوم تلقائياً.")
                        st.rerun()
                else:
                    st.error(f"❌ الملف المرفوع يفتقد إلى بعض الأعمدة الأساسية. تأكد من مطابقة أسماء الأعمدة لـ: {missing_cols}")
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء قراءة الملف: {e}")

    # التبويب الرابع للمسؤول: حذف منتج
    with admin_tab4:
        st.subheader("🗑️ حذف منتج نهائياً")
        product_to_delete = st.selectbox("اختر المنتج المراد إزالته تماماً:", options=st.session_state.products_db['اسم النوع'].unique() if not st.session_state.products_db.empty else ["لا توجد منتجات"])
        
        if st.button("🗑️ تأكيد الحذف النهائي") and not st.session_state.products_db.empty:
            st.session_state.products_db = st.session_state.products_db[st.session_state.products_db['اسم النوع'] != product_to_delete]
            st.success(f"🗑️ تم حذف المنتج بنجاح.")
            st.rerun()

else:
    if password_input:
        st.sidebar.error("❌ الكود السري غير صحيح. صلاحيات التعديل والرفع مقفلة حالياً.")
      
