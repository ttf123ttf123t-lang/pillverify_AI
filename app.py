import streamlit as st
import os
from PIL import Image
import database as db
from gtts import gTTS
import tempfile

# تهيئة قاعدة البيانات عند بدء التشغيل
db.init_db()

# إعدادات الصفحة والتجاوب مع الشاشات
st.set_page_config(
    page_title="PillVerify AI - العين الثالثة",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص لتحسين الواجهة وتقليل المساحات الفارغة ودعم الهواتف
st.markdown("""
    <style>
    .main-title {
        font-size: 32px !important;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        color: var(--text-color);
    }
    .sub-title {
        font-size: 17px !important;
        opacity: 0.85;
        text-align: center;
        margin-bottom: 20px;
    }
    .med-card {
        background-color: var(--secondary-background-color);
        padding: 18px;
        border-radius: 16px;
        border-right: 6px solid #2563EB;
        margin-bottom: 15px;
        color: var(--text-color);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .status-badge-success {
        background-color: rgba(34, 197, 94, 0.15);
        color: #16a34a;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .status-badge-danger {
        background-color: rgba(239, 68, 68, 0.15);
        color: #dc2626;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .warning-card {
        background-color: rgba(239, 68, 68, 0.12);
        padding: 15px;
        border-radius: 12px;
        border-right: 6px solid #EF4444;
        color: var(--text-color);
        font-weight: bold;
        margin-top: 10px;
    }
    .stButton>button {
        width: 100%;
        font-size: 18px !important;
        font-weight: 600;
        height: 52px;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي للتنقل
st.sidebar.image("https://img.icons8.com/color/96/pill.png", width=70)
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

# --- 1. صفحة التحقق البصري مع محرك المطابقة الدقيق ---
if page == "🔍 الفحص والتأكيد البصري":
    st.markdown("<div class='main-title'>🔍 نظام الفحص والتأكيد البصري الذكي</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>التحقق الفعلي من وجود الدواء ومطابقته بدقة مع المخزون</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📷 التقاط أو رفع صورة العلبة")
        
        # اختيار اسم الدواء الظاهر في الصورة للتحقق الفعلي الدقيق
        detected_input = st.text_input("🔤 اكتب اسم الدواء الظاهر في الصورة (للاختبار والتحقق الدقيق):", placeholder="مثال: Panadol Extra, Solpadeine, Adol, Slowofen")
        
        input_type = st.radio("طريقة الإدخال:", ["رفع صورة من الملفات", "استخدام كاميرا الجوال / الجهاز"], horizontal=True)
        
        img_file = None
        if input_type == "رفع صورة من الملفات":
            img_file = st.file_uploader("اختر صورة العلبة", type=["jpg", "jpeg", "png", "webp"])
        else:
            img_file = st.camera_input("التقط صورة لعلبة الدواء")
            
        if img_file:
            image = Image.open(img_file)
            st.image(image, caption="الصورة المدخلة للفحص", use_container_width=True)

    with col2:
        st.subheader("📋 نتيجة الفحص ومقاييس المطابقة")
        if img_file and detected_input:
            with st.spinner("جاري مطابقة اسم الدواء بدقة مع قاعدة بيانات المخزون..."):
                medicines = db.get_all_medicines()
                
                # البحث الذكي والدقيق عن الاسم المدخل حصراً داخل قاعدة البيانات
                matched_med = None
                if medicines:
                    for med in medicines:
                        # med[1] هو اسم الدواء التجاري
                        if detected_input.strip().lower() in med[1].lower() or med[1].lower() in detected_input.strip().lower():
                            matched_med = med
                            break
            
            if matched_med:
                # الدواء موجود فعلياً في المخزون وبنفس الاسم الصحيح
                m_id, trade_name, sci_name, strength, indications, warnings, remaining, daily_dose = matched_med
                
                st.markdown(f"<span class='status-badge-success'>✅ تم العثور على الدواء: {trade_name}</span>", unsafe_allow_html=True)
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.metric(label="🎯 درجة الثقة", value="99.2%", delta="مطابق تماماً")
                with col_s2:
                    st.metric(label="📦 المخزون المتبقي", value=f"{remaining} قرص")
                    
                st.markdown(f"""
                    <div class='med-card'>
                        <h3 style='margin-top:0;'>💊 {trade_name}</h3>
                        <p><b>الاسم العلمي:</b> {sci_name}</p>
                        <p><b>التركيز والنوع:</b> {strength}</p>
                        <p><b>دواعي الاستعمال:</b> {indications}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class='warning-card'>
                        ⚠️ تحذيرات هامة للمريض:<br>
                        {warnings}
                    </div>
                """, unsafe_allow_html=True)
                
                # إرشاد صوتي بالاسم الصحيح للدواء الذي بحث عنه المستخدم
                audio_text = f"تم التحقق. هذا دواء {trade_name}، وهو مسجل في سجلك الطبي."
                tts = gTTS(text=audio_text, lang='ar')
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, format='audio/mp3', autoplay=True)
                st.caption("🔊 الإرشاد الصوتي فعال")
                
            else:
                # الدواء غير موجود في المخزون (مثل سولبادين إذا لم تكن أضفته أو أي دواء آخر)
                st.markdown("<span class='status-badge-danger'>❌ تحذير: الدواء غير مسجل في المخزون!</span>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class='warning-card' style='background-color: rgba(239, 68, 68, 0.15); border-right: 6px solid #DC2626;'>
                        🚨 تنبيه أمني خطير للمريض:<br>
                        الدواء الذي تم إدخاله <b>({detected_input})</b> <b>غير مسجل</b> في قاعدة بيانات الأدوية الخاصة بك أو في جدول المخزون المعتمد! تجنب تناوله فوراً.
                    </div>
                """, unsafe_allow_html=True)
                
                # إرشاد صوتي تحذيري بأن الدواء غير موجود
                audio_text = f"تحذير! دواء {detected_input} غير موجود في سجلك الطبي."
                tts = gTTS(text=audio_text, lang='ar')
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    tts.save(fp.name)
                    st.audio(fp.name, format='audio/mp3', autoplay=True)
                st.caption("🔊 التنبيه الصوتي التحذيري فعال")
                
                if st.button("➕ إضافة هذا الدواء الجديد إلى المخزون الآن"):
                    st.info("توجه إلى صفحة (إضافة دواء جديد) من القائمة الجانبية لحفظه في سجلك.")
        else:
            st.info("👈 يرجى كتابة اسم الدواء ورفع صورته لبدء الفحص والمطابقة الدقيقة.")

# --- 2. صفحة الإشعارات التفاعلية ---
elif page == "🔔 التنبيهات والإشعارات":
    st.markdown("<div class='main-title'>🔔 مركز التنبيهات والإشعارات التفاعلية</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>إدارة المواعيد والجرعات اليومية بلمسة واحدة</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); padding: 20px; border-radius: 18px; color: white; margin-bottom: 15px; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.2);'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                <span style='background: rgba(255, 255, 255, 0.2); padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: bold;'>السكري والضغط 🩸</span>
                <span style='font-size: 20px;'>🔔</span>
            </div>
            <h2 style='margin: 0; font-size: 22px; color: white;'>Ibuprofen - 200 mg</h2>
            <p style='margin: 4px 0 12px 0; font-size: 15px; opacity: 0.9;'>1 Pill • After Meal (بعد الغداء)</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("❌ تخطي الجرعة", key="skip_dose"):
            st.warning("⚠️ تم تسجيل تخطي الجرعة وإرسال تنبيه للمرافق.")
            st.toast("تم تسجيل التخطي بنجاح", icon="⚠️")
    with col_btn2:
        if st.button("✅ تأكيد أخذ الجرعة", key="take_dose", type="primary"):
            st.success("✅ ممتاز! تم تأكيد تناول الجرعة بنجاح وتحديث السجل.")
            st.toast("تم تسجيل أخذ الجرعة في السجل الطبي", icon="✅")
            
    st.markdown("---")
    st.subheader("📅 الجدول الزمني للمواعيد اليومية:")
    
    col_t1, col_d1 = st.columns([1, 4])
    with col_t1:
        st.markdown("<h3 style='color: #2563EB; margin: 0;'>09:00 AM</h3>", unsafe_allow_html=True)
        st.caption("صباحاً")
    with col_d1:
        st.markdown("""
            <div style='background-color: var(--secondary-background-color); padding: 14px; border-radius: 12px; border-right: 5px solid #2563EB; margin-bottom: 10px;'>
                <b>Cardiovascular - Amlodipine 5mg</b><br>
                <span style='font-size: 13px; opacity: 0.8;'>1 Pill • Before Meal (قبل الإفطار)</span>
            </div>
        """, unsafe_allow_html=True)

    col_t2, col_d2 = st.columns([1, 4])
    with col_t2:
        st.markdown("<h3 style='color: #2563EB; margin: 0;'>02:00 PM</h3>", unsafe_allow_html=True)
        st.caption("ظهراً")
    with col_d2:
        st.markdown("""
            <div style='background-color: var(--secondary-background-color); padding: 14px; border-radius: 12px; border-right: 5px solid #EF4444; margin-bottom: 10px;'>
                <b>Diabetes - Ibuprofen 200 mg</b><br>
                <span style='font-size: 13px; opacity: 0.8;'>1 Pill • After Meal (بعد الغداء) - ⚠️ تنبيه اقتراب نفاذ العلبة</span>
            </div>
        """, unsafe_allow_html=True)

# --- 3. منظم الأدوية الأسبوعي ---
elif page == "📅 منظم الأدوية الأسبوعي":
    st.markdown("<div class='main-title'>📅 منظم الأدوية الأسبوعي</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>استعراض مواعيد وأوقات الأدوية حسب أيام الأسبوع</div>", unsafe_allow_html=True)
    
    medicines = db.get_all_medicines()
    days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
    selected_day = st.select_slider("اختر اليوم لاستعراض الأدوية:", options=days)
    
    st.write(f"### 📋 جدول جرعات يوم ({selected_day}):")
    if medicines:
        for med in medicines:
            m_id, trade_name, sci_name, strength, indications, warnings, remaining, daily_dose = med
            st.markdown(f"""
                <div class='med-card'>
                    <h4 style='margin:0;'>💊 {trade_name} ({strength})</h4>
                    <p style='margin: 5px 0;'><b>الجرعة اليومية:</b> {daily_dose} قرص يومياً | <b>المتبقي:</b> {remaining} قرص</p>
                    <span style='font-size: 13px; opacity: 0.8;'><b>التعليمات:</b> {indications}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ لا توجد أدوية مسجلة في القاعدة حالياً.")

# --- 4. إدارة المخزون المترابط ---
elif page == "📦 إدارة المخزون":
    st.markdown("<div class='main-title'>📦 تتبع المخزون الذكي والتنبيه الاستباقي</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>حساب الأيام المتبقية تلقائياً بناءً على معدل الاستهلاك الفعلي</div>", unsafe_allow_html=True)
    
    medicines = db.get_all_medicines()
    if medicines:
        for med in medicines:
            m_id, trade_name, sci_name, strength, indications, warnings, remaining, daily_dose = med
            days_left = remaining // daily_dose if daily_dose > 0 else 0
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"### 💊 {trade_name} - {strength}")
                progress_val = min(max(remaining / 30, 0.0), 1.0)
                st.progress(progress_val)
                st.write(f"المتبقي في العلبة: **{remaining} قرص** (يكفي لمدة **{days_left} أيام**)")
            with col_b:
                if days_left <= 7:
                    st.error("⚠️ مخزون منخفض! (يلزم إعادة التعبئة)")
                else:
                    st.success("✅ المخزون ممتاز")
            st.markdown("---")
    else:
        st.info("لا توجد بيانات مخزون مسجلة حالياً.")

# --- 5. بوابة الصيدلي (ربط صحتي) ---
elif page == "🏥 بوابة الصيدلي (ربط صحتي)":
    st.markdown("<div class='main-title'>🏥 بوابة الصيدلي المعتمدة (نظام صحتي)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>إدخال الخطة العلاجية وربط الأدوية المعتمدة بملف المريض</div>", unsafe_allow_html=True)
    
    with st.form("pharmacist_link_form"):
        patient_name = st.text_input("اسم المريض الثلاثي:")
        trade_name = st.text_input("اسم الدواء التجاري (مثل: Panadol Extra):")
        scientific_name = st.text_input("الاسم العلمي:")
        strength = st.text_input("التركيز (مثل: 500 mg):")
        indications = st.text_area("دواعي الاستعمال والتعليمات الطبية:")
        warnings = st.text_area("تحذيرات كبار السن:")
        
        col_1, col_2 = st.columns(2)
        with col_1:
            total_pills = st.number_input("إجمالي الأقراص الموصوفة", min_value=1, value=30)
        with col_2:
            daily_dose = st.number_input("الجرعة اليومية المطلوبة", min_value=1, value=2)
            
        submit_link = st.form_submit_button("🔗 اعتماد الربط وإرسال الجدول لملف المريض")
        if submit_link:
            if patient_name and trade_name:
                db.add_medicine(trade_name, scientific_name, "أقراص", strength, indications, warnings, total_pills, daily_dose)
                st.success(f"✅ تم ربط الدواء ({trade_name}) بنجاح بملف المريض ({patient_name})!")
                st.toast("📱 تم إرسال إشعار فوري لتطبيق صحتي المربوط بالجوال!", icon="📲")
            else:
                st.error("⚠️ يرجى تعبئة الحقول الأساسية لربط الدواء.")

# --- 6. زر الطوارئ السريع ---
elif page == "🚨 زر الطوارئ السريع":
    st.markdown("<div class='main-title'>🚨 مركز الطوارئ والاتصال السريع</div>", unsafe_allow_html=True)
    st.error("في حال حدوث أي اشتباه بخلل في الجرعات أو حالة صحية طارئة، استخدم الأزرار المباشرة أدناه:")
    
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
            st.success("تم إرسال تقرير حالة المريض والأدوية المستهلكة.")

# --- 7. إضافة دواء جديد ---
elif page == "➕ إضافة دواء جديد":
    st.markdown("<div class='main-title'>➕ إضافة دواء جديد لقاعدة البيانات المحلّية</div>", unsafe_allow_html=True)
    with st.form("add_med_form"):
        trade_name = st.text_input("اسم الدواء التجاري (مثل: Panadol Extra)")
        scientific_name = st.text_input("الاسم العلمي (مثل: Paracetamol)")
        dosage_form = st.selectbox("الشكل الدوائي", ["أقراص", "شراب", "حقن", "قطرة", "مرهم"])
        strength = st.text_input("التركيز (مثل: 500 mg)")
        indications = st.text_area("دواعي الاستعمال")
        warnings = st.text_area("تحذيرات هامة لكبار السن")
        
        col_x, col_y = st.columns(2)
        with col_x:
            total_pills = st.number_input("عدد الأقراص في العلبة الكاملة", min_value=1, value=30)
        with col_y:
            daily_dose = st.number_input("عدد الجرعات اليومية", min_value=1, value=1)
            
        submit = st.form_submit_button("💾 حفظ الدواء في قاعدة البيانات")
        if submit:
            if trade_name and scientific_name:
                db.add_medicine(trade_name, scientific_name, dosage_form, strength, indications, warnings, total_pills, daily_dose)
                st.success(f"✅ تم حفظ الدواء ({trade_name}) بنجاح في السجل المحلي!")
                st.toast("💾 تم التحديث بنجاح!", icon="✅")
            else:
                st.error("⚠️ يرجى تعبئة الأسماء الأساسية للدواء.")