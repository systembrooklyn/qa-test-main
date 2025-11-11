import google.generativeai as genai
import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import mimetypes 
from datetime import datetime

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No GEMINI_API_KEY set in .env file")

genai.configure(api_key=api_key)

# دالة لقراءة القواعد من الملف
def load_rules():
    """تحميل القواعد من ملف rules.txt"""
    try:
        with open('rules.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # إذا لم يوجد الملف، نرجع القواعد الافتراضية
        return """أنت مدير جودة خبير ومحلل مكالمات في "بروكلين بيزنس سكول" لمنحة MBA.
مهمتك هي تقييم أداء الموظف في المكالمة التالية بدقة شديدة بناءً على المعايير المفصلة أدناه. يجب أن تكون صارماً في تطبيق القواعد."""
    except Exception as e:
        print(f"Error loading rules: {e}")
        return ""

# تحميل القواعد عند بدء التشغيل
RULES_PROMPT = load_rules()

model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-05-20")

app = Flask(__name__)
CORS(app)

# تغيير Jinja2 delimiters لتجنب تعارض مع Vue.js
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
app.jinja_env.block_start_string = '[%'
app.jinja_env.block_end_string = '%]'

@app.route('/')
def home():
    """صفحة الواجهة الرئيسية"""
    return render_template('index.html')

@app.route('/rules')
def rules_page():
    """صفحة إدارة القواعد"""
    return render_template('rules.html')

@app.route('/current_rules', methods=['GET'])
def get_current_rules():
    """الحصول على القواعد الحالية"""
    try:
        rules = load_rules()
        return jsonify({"rules": rules}), 200
    except Exception as e:
        return jsonify({"error": f"Error loading rules: {e}"}), 500

@app.route('/enhance_rules', methods=['POST'])
def enhance_rules():
    """تحسين القواعد باستخدام AI"""
    try:
        data = request.get_json()
        raw_rules = data.get('rules', '')
        
        if not raw_rules:
            return jsonify({"error": "No rules provided"}), 400
        
        # برومبت لتحسين القواعد
        enhance_prompt = """أنت خبير في كتابة قواعد تقييم المكالمات. المطلوب منك تحسين وتنسيق النص التالي ليصبح في نفس الصيغة القياسية لقواعد التقييم.

المتطلبات:
1. يجب أن يكون التقييم من 10 درجات إجمالي
2. يجب تقسيم القواعد إلى أقسام واضحة مع درجات لكل قسم
3. يجب أن يكون هناك قسم "المطلوب" يوضح صيغة JSON المطلوبة للإرجاع
4. يجب أن يكون النص واضحاً ومفصلاً باللغة العربية
5. احافظ على نفس الأسلوب الاحترافي والصرامة في التطبيق

النص المراد تحسينه:
"""
        
        response = model.generate_content([enhance_prompt + raw_rules])
        enhanced_rules = response.text.strip()
        
        return jsonify({"enhanced_rules": enhanced_rules}), 200
        
    except Exception as e:
        print(f"Error enhancing rules: {e}")
        return jsonify({"error": f"Error enhancing rules: {e}"}), 500

@app.route('/save_rules', methods=['POST'])
def save_rules():
    """حفظ القواعد الجديدة"""
    try:
        data = request.get_json()
        new_rules = data.get('rules', '')
        
        if not new_rules:
            return jsonify({"error": "No rules provided"}), 400
        
        # عمل نسخة احتياطية قبل الحفظ
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"rules_backup_{timestamp}.txt"
            if os.path.exists('rules.txt'):
                with open('rules.txt', 'r', encoding='utf-8') as f:
                    backup_content = f.read()
                with open(backup_filename, 'w', encoding='utf-8') as f:
                    f.write(backup_content)
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
        
        # حفظ القواعد الجديدة
        with open('rules.txt', 'w', encoding='utf-8') as f:
            f.write(new_rules)
        
        # تحديث المتغير في الذاكرة
        global RULES_PROMPT
        RULES_PROMPT = new_rules
        
        return jsonify({"message": "Rules saved successfully"}), 200
        
    except Exception as e:
        print(f"Error saving rules: {e}")
        return jsonify({"error": f"Error saving rules: {e}"}), 500

@app.route('/analyze_call', methods=['POST'])
def analyze_call_handler():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files['file']

    try:
        print("Sending file and prompt to Gemini for analysis...")
        
        audio_data = audio_file.read()
        
        audio_file_part = {
            "mime_type": audio_file.mimetype,
            "data": audio_data
        }

        response = model.generate_content(
            [
                RULES_PROMPT,
                audio_file_part
            ]
        )
        
        json_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        # تحويل النص إلى كائن JSON وإرجاعه بصيغة صحيحة
        try:
            data = json.loads(json_response)
            return jsonify(data), 200
        except json.JSONDecodeError as je:
            print(f"JSON Parse Error: {je}")
            print(f"Response text: {json_response}")
            return jsonify({"error": "Failed to parse AI response as JSON", "raw_response": json_response}), 500

    except Exception as e:
        print(f"!!!!!!!! AN ERROR OCCURRED !!!!!!!!\n{e}\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return jsonify({"error": f"An internal error occurred during analysis: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

