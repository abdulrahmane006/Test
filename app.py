import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة كاملة
st.set_page_config(page_title="نظام إدارة مخزن التوبات الذكي", page_icon="📦", layout="wide")

# تخصيص اتجاه النصوص والتصميم ليتناسب مع اللغة العربية (RTL)
st.markdown("""
    <style>
    .stApp {
        direction: RTL;
        text-align: right;
    }
    div[data-testid="stForm"] {
        direction: RTL;
        text-align: right;
    }
    div[data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# 1. تهيئة قاعدة البيانات الافتراضية مع إضافة حقل "تاريخ آخر تعديل"
if 'products_db' not in st.session_state:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.products_db = pd.DataFrame([
        {"الكود": "101", "اسم النوع": "توب قطن حريمي", "اللون": "أسود", "المخزن": "مخزن أ", "العدد المتوفر": 25, "تاريخ آخر تعديل": current_time},
        {"الكود": "102", "اسم النوع": "توب صوف رجالي", "اللون": "أزرق", "المخزن": "مخزن ب", "العدد المتوفر": 14, "تاريخ آخر تعديل": current_time},
        {"الكود": "103", "اسم النوع": "توب سبورت", "اللون": "أحمر", "المخزن": "مخزن أ", "العدد المتوفر": 50, "تاريخ آخر تعديل": current_time},
    ])

# الكود السري الخاص بالمسؤول (يمكنك تعديله من هنا)
ADMIN_PASSWORD = "admin"

# العنوان الرئيسي للموقع
st.title("📦 نظام جرد وبحث المنتجات الذكي المحترف")
st.write("---")

# -------------------------------------------------------------
# الجزء الأول: الواجهة الرئيسية المتاحة للجميع (عمال ومسؤولين)
# -------------------------------------------------------------

# إنشاء تبويبات في الصفحة الرئيسية لفصل البحث عن عرض كل المنتجات
main_tab1, main_tab2 = st.tabs(["🔍 البحث السريع", "📋 استعراض كافة المنتجات"])

with main_tab1:
    st.header("🔍 البحث في المخزن")
    # خانة البحث الذكي
    search_query = st.text_input("أدخل اسم النوع أو كود المنتج للبحث المباشر:", placeholder="اكتب هنا للبحث...")
    
    df = st.session_state.products_db
    if search_query:
        # تصفية شاملة بناء على الكود أو اسم النوع
        filtered_df = df[
            df['اسم النوع'].str.contains(search_query, case=False, na=False) | 
            df['الكود'].astype(str).str.contains(search_query, case=False, na=False)
        ]
    else:
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
      
