import sqlite3
import os

DB_PATH = os.path.join("data", "medicines.db")

def init_db():
    """إنشاء قاعدة البيانات والجداول الأساسية إذا لم تكن موجودة"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # جدول الأدوية الأساسي
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_name TEXT NOT NULL,
            scientific_name TEXT NOT NULL,
            dosage_form TEXT,
            strength TEXT,
            indications TEXT,
            warnings TEXT,
            total_pills INTEGER DEFAULT 30,
            remaining_pills INTEGER DEFAULT 30,
            daily_dose INTEGER DEFAULT 1
        )
    ''')
    
    # إضافة بيانات عينات أولية للتجربة إذا كان الجدول فارغاً
    cursor.execute("SELECT COUNT(*) FROM medicines")
    if cursor.fetchone()[0] == 0:
        sample_medicines = [
            ("Panadol Extra", "Paracetamol / Caffeine", "أقراص", "500 mg", "مسكن للألم ومخفف للحرارة والصداع", "لا يتناول أكثر من 8 أقراص يومياً. يحذر مع أمراض الكبد.", 20, 15, 2),
            ("Aspirin", "Acetylsalicylic Acid", "أقراص", "100 mg", "ميوعة الدم والوقاية من الجلطات", "يؤخذ بعد الأكل مباشرة لتجنب تهيج المعدة.", 30, 8, 1),
            ("Lipitor", "Atorvastatin", "أقراص", "20 mg", "خافض للكلسترول والدهون الثلاثية", "يؤخذ عادة مساءً. يرجى مراجعة وظائف الكبد دورياً.", 30, 25, 1),
            ("Concor", "Bisoprolol", "أقراص", "5 mg", "علاج ارتفاع ضغط الدم وتنظيم ضربات القلب", "لا توقف الدواء فجأة دون استشارة الطبيب.", 30, 5, 1)
        ]
        cursor.executemany('''
            INSERT INTO medicines 
            (trade_name, scientific_name, dosage_form, strength, indications, warnings, total_pills, remaining_pills, daily_dose)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_medicines)
        
    conn.commit()
    conn.close()

def get_all_medicines():
    """استرجاع كافة الأدوية المسجلة"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, trade_name, scientific_name, strength, indications, warnings, remaining_pills, daily_dose FROM medicines")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_medicine(trade_name, scientific_name, dosage_form, strength, indications, warnings, total_pills, daily_dose):
    """إضافة دواء جديد لقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicines 
        (trade_name, scientific_name, dosage_form, strength, indications, warnings, total_pills, remaining_pills, daily_dose)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (trade_name, scientific_name, dosage_form, strength, indications, warnings, total_pills, total_pills, daily_dose))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ تم إنشاء قاعدة البيانات المحلية بنجاح!")