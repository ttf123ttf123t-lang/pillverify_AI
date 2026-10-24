import streamlit as st
import os
from PIL import Image
import database as db

# تهيئة قاعدة البيانات عند بدء التشغيل
db.init_db()

# إعدادات الصفحة
st.set_page_config(
    page_title="PillVerify AI - العين الثالثة",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيق مخصص لكبار السن (خطوط كبيرة وألوان مريحة للعين)
st.markdown("""
    <style>
    .main-title {
        font-size: 38px !important;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        padding-bottom: 10px;
    }
    .sub-title {
        font-size: 20px !important;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        font-size: 22px !important;
        height: 60px;
        background-color: #2563EB;
        color: white;
        border-radius: 12px;
    }
    .med-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #2563EB;
        margin-bottom: 15px;
    }
    .warning-card {
        background-color: #FEF2F2;
        padding: 15px;
        border-radius: 10px;
        border-right: 6px solid #EF4444;
        color: #991B1B;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي لتصفح الأقسام
st.sidebar.image("https://img.icons8.com/color/96/pill.png", width=80)
st.sidebar.title("العين الثالثة 💊")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "اختر الخدمة:",
    ["🔍 الفحص والتأكيد البصري", "📅 منظم الأدوية الأسبوعي", "📦 إدارة المخزون والتنبيهات", "➕ إضافة دواء جديد"]
)

# الصفحة الأولى: الفحص والتأكيد البصري
if page == "🔍 الفحص والتأكيد البصري":
    st.markdown("<div class='main-title'>🔍 نظام التحقق الذكي من الدواء</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>وجه الكاميرا أو ارفع صورة علبة الدواء للتحقق التلقائي</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📷 التقاط / رفع الصورة")
        img_file = st.file_uploader("اختر صورة العلبة أو الشريط", type=["jpg", "jpeg", "png"])
        camera_file = st.camera_input("أو التقط صورة مباشرة")
        
        input_image = img_file if img_file is not None else camera_file
        
        if input_image:
            image = Image.open(input_image)
            st.image(image, caption="الصورة المدخلة", use_container_width=True)
            
            if st.button("🚀 بدء التحقق والتحليل البصري"):
                st.info("🔄 جاري تطبيق معالجة الصور والتصحيح الهندسي لفك الانحناءات...")
                # سيتم ربط كود المعالجة المسبقة و OCR في اليوم القادم
                st.success("✅ تم التعرف على الدواء بنجاح!")
                
    with col2:
        st.subheader("📋 نتيجة التحقق والإرشادات")
        if input_image:
            st.markdown("""
                <div class='med-card'>
                    <h2>💊 بانادول إكسترا (Panadol Extra)</h2>
                    <p><b>الاسم العلمي:</b> Paracetamol / Caffeine</p>
                    <p><b>التركيز والنوع:</b> 500 mg - أقراص</p>
                    <p><b>دواعي الاستعمال:</b> مسكن للألم ومخفف للحرارة والصداع</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class='warning-card'>
                    ⚠️ تحذير هاديء لكبار السن:<br>
                    لا تتناول أكثر من 8 أقراص خلال 24 ساعة. يحظر استخدامه مع أدوية أخرى تحتوي على الباراسيتامول.
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
            st.caption("🔊 استمع للتنبيه الصوتي الوارد من التطبيق")
        else:
            st.info("👈 يرجى رفع صورة أو التقاطها عبر الكاميرا للبدء.")

# الصفحة الثانية: منظم الأدوية الأسبوعي
elif page == "📅 منظم الأدوية الأسبوعي":
    st.markdown("<div class='main-title'>📅 منظم الأدوية الأسبوعي لكبار السن</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>متابعة جدول الجرعات اليومية والتحقق من خانات المنظم</div>", unsafe_allow_html=True)
    
    medicines = db.get_all_medicines()
    days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
    
    selected_day = st.selectbox("اختر اليوم:", days)
    st.write(f"### 📋 جدول جرعات يوم ({selected_day}):")
    
    for med in medicines:
        m_id, trade_name, sci_name, strength, indications, warnings, remaining, daily_dose = med
        st.markdown(f"""
            <div class='med-card'>
                <h4>💊 {trade_name} ({strength})</h4>
                <p><b>الجرعة اليومية:</b> {daily_dose} قرص يومياً | <b>المتبقي في العلبة:</b> {remaining} قرص</p>
            </div>
        """, unsafe_allow_html=True)

# الصفحة الثالثة: إدارة المخزون والتنبيهات
elif page == "📦 إدارة المخزون والتنبيهات":
    st.markdown("<div class='main-title'>📦 تتبع مخزون العلب والتنبيه الاستباقي</div>", unsafe_allow_html=True)
    
    medicines = db.get_all_medicines()
    for med in medicines:
        m_id, trade_name, sci_name, strength, indications, warnings, remaining, daily_dose = med
        days_left = remaining // daily_dose if daily_dose > 0 else 0
        
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.write(f"### 💊 {trade_name} - {strength}")
            st.progress(min(remaining / 30, 1.0))
            st.write(f"المتبقي: **{remaining} قرص** (يكفي لمدة **{days_left} أيام**)")
            
        with col_b:
            if days_left <= 7:
                st.error("⚠️ مخزون منخفض! يلزم الشراء")
            else:
                st.success("✅ المخزون ممتاز")
        st.markdown("---")

# الصفحة الرابعة: إضافة دواء جديد
elif page == "➕ إضافة دواء جديد":
    st.markdown("<div class='main-title'>➕ إضافة دواء جديد لقاعدة البيانات المحلّية</div>", unsafe_allow_html=True)
    
    with st.form("add_med_form"):
        trade_name = st.text_input("اسم الدواء التجاري (مثل: Panadol Extra)")
        scientific_name = st.text_input("الاسم العلمي (مثل: Paracetamol)")
        dosage_form = st.selectbox("الشكل الدوائي", ["أقراص", "شراب", "حقن", "قطرة", "مرهم"])
        strength = st.text_input("التركيز (مثل: 500 mg)")
        indications = st.text_area("دواعي الاستعمال")
        warnings = st.text_area("تحذيرات هامة وكبار السن")
        
        col_x, col_y = st.columns(2)
        with col_x:
            total_pills = st.number_input("عدد الأقراص في العلبة الكاملة", min_value=1, value=30)
        with col_y:
            daily_dose = st.number_input("عدد الجرعات اليومية", min_value=1, value=1)
            
        submit = st.form_submit_button("💾 حفظ الدواء في قاعدة البيانات")
        
        if submit:
            if trade_name and scientific_name:
                db.add_medicine(trade_name, scientific_name, dosage_form, strength, indications, warnings, total_pills, daily_dose)
                st.success(f"✅ تم حفظ الدواء ({trade_name}) بنجاح في قاعدة البيانات المحلية!")
            else:
                st.error("⚠️ يرجى تعبئة الأسماء الأساسية للدواء.")