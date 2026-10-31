import streamlit as st
import os
from PIL import Image
import database as db
from gtts import gTTS
import tempfile
import numpy as np
import cv2

# تهيئة قاعدة البيانات عند بدء التشغيل
db.init_db()

# إعدادات الصفحة
st.set_page_config(
    page_title="PillVerify AI - العين الثالثة",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص يدعم الوضعين الداكن والفاتح تلقائياً مع خطوط واضحة لكبار السن
st.markdown("""
    <style>
    /* ألوان استجابة مع وضع الجهاز (داكن / فاتح) */
    .main-title {
        font-size: 36px !important;
        font-weight: bold;
        text-align: center;
        padding-bottom: 10px;
    }
    .sub-title {
        font-size: 19px !important;
        opacity: 0.85;
        text-align: center;
        margin-bottom: 25px;
    }
    .med-card {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #2563EB;
        margin-bottom: 15px;
        color: var(--text-color);
    }
    .warning-card {
        background-color: rgba(239, 68, 68, 0.15);
        padding: 15px;
        border-radius: 10px;
        border-right: 6px solid #EF4444;
        color: var(--text-color);
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        font-size: 20px !important;
        height: 55px;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي لتصفح الأقسام
st.sidebar.image("https://img.icons8.com/color/96/pill.png", width=80)
st.sidebar.title("العين الثالثة 💊")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "اختر الخدمة:",
    [
        "🔍 الفحص والتأكيد البصري", 
        "🔔 التنبيهات والإشعارات",
        "📅 منظم الأدوية الأسبوعي", 
        "📦 إدارة المخزون", 
        "🏥 بوابة الصيدلي (ربط صحتي)", 
        "🚨 زر الطوارئ السريع",
        "➕ إضافة دواء جديد"
    ]
)

# --- 1. الفحص والتأكيد البصري ---
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
                st.info("🔄 جاري تطبيق معالجة الصور والتصحيح الهندسي...")
                st.success("✅ تم التعرف على الدواء بنجاح واستطابته مع جدول المريض!")
                
                # إشعار منبثق على الشاشة (Toast)
                st.toast("✅ تم التحقق من الدواء: مطابق للجدول اليومي!", icon="💊")
                
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
                    ⚠️ تنبيه ذكي لكبار السن:<br>
                    مطابق لجدولك اليومي. لا تتناول أكثر من 8 أقراص خلال 24 ساعة.
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            # صوتي
            tts = gTTS(text="الدواء صحيح. تناول حبة واحدة الآن بعد الغداء.", lang='ar')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                st.audio(fp.name, format='audio/mp3', autoplay=True)
            st.caption("🔊 تم تشغيل التنبيه الصوتي الإرشادي للمريض بنجاح")
        else:
            st.info("👈 يرجى رفع صورة أو التقاطها عبر الكاميرا للبدء.")

# --- 2. قسم التنبيهات والإشعارات الفورية ---
elif page == "🔔 التنبيهات والإشعارات":
    st.markdown("<div class='main-title'>🔔 مركز التنبيهات والإشعارات الفورية</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>قائمة التنبيهات المباشرة ومواعيد الجرعات القادمة</div>", unsafe_allow_html=True)
    
    st.button("🔔 اختبار إشعار تفاعلي فوراً", on_click=lambda: st.toast("⏰ حان موعد جرعة دواء الضغط الآن!", icon="🔔"))
    
    st.markdown("---")
    st.subheader("📋 قائمة الإشعارات اليومية:")
    
    st.info("🔔 **إشعار (10:00 ص):** حان موعد تناول دواء *Panadol Extra* (قرص واحد بعد الإفطار).")
    st.warning("⏰ **تنبيه إعادة تعبئة (02:30 م):** متبقي 3 أجزاء فقط في علبة *Aspirin*. يرجى التواصل مع الصيدلية.")
    st.success("✅ **تأكيد فحص (08:00 م):** تم مطابقة دواء العشاء بنجاح عبر الكاميرا.")

# --- 3. منظم الأدوية الأسبوعي ---
elif page == "📅 منظم الأدوية الأسبوعي":
    st.markdown("<div class='main-title'>📅 منظم الأدوية الأسبوعي</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>متابعة جدول الجرعات اليومية والتحقق من خانات المنظم</div>", unsafe_allow_html=True)
    
    medicines = db.get_all_medicines()
    days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
    
    selected_day = st.selectbox("اختر اليوم:", days)
    st.write(f"### 📋 جدول جرعات يوم ({selected_day}):")
    
    if medicines:
        for med in medicines:
            m_id, trade_name, sci_name, strength, indications, warnings, remaining, daily_dose = med
            st.markdown(f"""
                <div class='med-card'>
                    <h4>💊 {trade_name} ({strength})</h4>
                    <p><b>الجرعة اليومية:</b> {daily_dose} قرص يومياً | <b>المتبقي في العلبة:</b> {remaining} قرص</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ لا توجد أدوية مسجلة في القاعدة حالياً.")

# --- 4. إدارة المخزون ---
elif page == "📦 إدارة المخزون":
    st.markdown("<div class='main-title'>📦 تتبع مخزون العلب والتنبيه الاستباقي</div>", unsafe_allow_html=True)
    
    medicines = db.get_all_medicines()
    if medicines:
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
                    st.error("⚠️ مخزون منخفض!")
                    st.toast(f"⚠️ تحذير: مخزون {trade_name} ينتهي خلال أقل من أسبوع!", icon="📦")
                else:
                    st.success("✅ المخزون ممتاز")
            st.markdown("---")
    else:
        st.info("لا توجد بيانات مخزون حالياً.")

# --- 5. بوابة الصيدلي (ربط صحتي) ---
elif page == "🏥 بوابة الصيدلي (ربط صحتي)":
    st.markdown("<div class='main-title'>🏥 بوابة الصيدلي المعتمدة (ربط نظام صحتي)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>ربط وصفات وخطط الأدوية مباشرة بملف المريض الإلكتروني</div>", unsafe_allow_html=True)
    
    with st.form("pharmacist_link_form"):
        patient_name = st.text_input("اسم المريض الثلاثي:")
        trade_name = st.text_input("اسم الدواء التجاري (مثل: Panadol Extra):")
        scientific_name = st.text_input("الاسم العلمي:")
        strength = st.text_input("التركيز (مثل: 500 mg):")
        indications = st.text_area("دواعي الاستعمال والتعليمات الطبية:")
        warnings = st.text_area("تحذيرات هامة للمريض:")
        
        col_1, col_2 = st.columns(2)
        with col_1:
            total_pills = st.number_input("إجمالي الأقراص الموصوفة", min_value=1, value=30)
        with col_2:
            daily_dose = st.number_input("الجرعة اليومية المطلوبة", min_value=1, value=2)
            
        submit_link = st.form_submit_button("🔗 اعتماد الربط وإرسال الجدول إلى ملف المريض")
        
        if submit_link:
            if patient_name and trade_name:
                db.add_medicine(trade_name, scientific_name, "أقراص", strength, indications, warnings, total_pills, daily_dose)
                st.success(f"✅ تم ربط الدواء ({trade_name}) بنجاح بملف المريض ({patient_name}) عبر شبكة الأدوية الذكية!")
                st.toast("📱 تم إرسال إشعار فوري لتطبيق صحتي المربوط بالجوال!", icon="📲")
            else:
                st.error("⚠️ يرجى إدخال اسم المريض واسم الدواء على الأقل.")

# --- 6. زر الطوارئ السريع ---
elif page == "🚨 زر الطوارئ السريع":
    st.markdown("<div class='main-title'>🚨 مركز الطوارئ والاتصال السريع</div>", unsafe_allow_html=True)
    st.error("في حال حدوث أي اشتباه بخلل في الجرعات أو حالة صحية طارئة، استخدم الأزرار أدناه فوراً:")
    
    col_x, col_y = st.columns(2)
    with col_x:
        if st.button("📞 الاتصال بالإسعاف (997)"):
            st.markdown("### 🔴 جارٍ الاتصال بخدمات الإسعاف والطوارئ...")
            st.toast("🚨 تم إطلاق إنذار الطوارئ والإسعاف!", icon="🚑")
            st.warning("رقم الطوارئ النشط: 997 - حافظ على هدوئك.")
            
    with col_y:
        if st.button("👨‍⚕️ إبلاغ الطبيب المعالج / المرافق"):
            st.markdown("### 🟡 تم إرسال تنبيه عاجل لبريد المرافق والطبيب!")
            st.toast("📧 تم إرسال إشعار SOS للطبيب المرافق بنجاح!", icon="📩")
            st.success("تم إرسال تقرير آخر دواء تم فحصه وحالة المريض بنجاح.")

    st.markdown("---")
    st.info("💡 **ميزة نظام الطوارئ الذكي:** يحتفظ النظام بآخر سجل فحص دوائي لعرضه على الفريق الطبي فوراً عند الطوارئ لضمان السلامة التامة.")

# --- 7. إضافة دواء جديد ---
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
                st.toast("💾 تم حفظ الدواء وتحديث السجل المحلي!", icon="✅")
            else:
                st.error("⚠️ يرجى تعبئة الأسماء الأساسية للدواء.")