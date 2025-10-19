import google.generativeai as genai
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import mimetypes 

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No GEMINI_API_KEY set in .env file")

genai.configure(api_key=api_key)

# --- تم تعديل نظام التقييم ليصبح من 10 درجات ---
RULES_PROMPT = """
أنت مدير جودة خبير ومحلل مكالمات في "بروكلين بيزنس سكول" لمنحة MBA.
مهمتك هي تقييم أداء الموظف في المكالمة التالية بدقة شديدة بناءً على المعايير المفصلة أدناه. يجب أن تكون صارماً في تطبيق القواعد.

**قواعد التقييم المفصلة (الإجمالي من 10 درجات):**

**1. بروتوكول الافتتاحية (2 درجة):**
   - **(0.5) التعريف بالمنحة:** هل ذكر الموظف اسم "منحة MBA" في بداية المكالمة؟
   - **(0.5) سؤال عن الاسم:** هل سأل الموظف عن اسم الطالب الثلاثي بوضوح؟
   - **(0.5) الترحيب بالاسم:** هل رحب الموظف بالطالب بعد معرفة اسمه؟
   - **(0.5) استئذان للوقت (للمكالمات الصادرة):** هل استأذن الموظف بدقيقتين من وقت الطالب؟

**2. الاحترافية واللغة (3 درجات):**
   - **(1) تجنب العامية والممنوعات:** هل تجنب الموظف تماماً كلمات مثل (ايه، اه، لأ، مش عارف/ة) والمصطلحات الدينية؟
   - **(1) عدم مقاطعة الطالب:** هل أعطى الموظف فرصة كاملة للطالب للحديث دون مقاطعة؟
   - **(0.5) وتيرة الكلام:** هل كانت سرعة كلام الموظف مناسبة؟
   - **(0.5) آداب الانتظار:** عند وضع الطالب في الانتظار، هل شكره الموظف على انتظاره عند العودة؟

**3. الالتزام بالاسكريبت وجودة المعلومات (3 درجات):**
   - **(1) شرح الاعتماد:** هل أوضح الموظف أهمية "اعتماد الشهادة"؟
   - **(0.5) شرح تكلفة المنحة:** هل استخدم الموظف صيغة "المنحة قبل وبعد الدعم" وتجنب كلمة "تكلفة"؟
   - **(0.5) استخدام اسم الطالب:** هل كرر الموظف اسم الطالب 3 مرات على الأقل؟
   - **(0.5) معلومات الاختبار:** هل اكتفى الموظف بذكر المعلومات الأساسية للاختبار دون الخوض في تفاصيل خاطئة؟
   - **(0.5) عرض تقديم استفسار:** هل عرض الموظف تقديم استفسار للإدارة؟

**4. بروتوكول الإنهاء (2 درجة):**
   - **(1) السؤال عن استفسارات أخرى:** هل سأل الموظف "هل لدى حضرتك أي استفسار آخر؟"
   - **(1) جملة الختام الرسمية:** هل أنهى الموظف المكالمة بجملة "شكراً لاتصالك ببروكلين بيزنس سكول"؟

**المطلوب:**
بعد تحليل المكالمة، قم بإرجاع تقييمك **فقط** بصيغة JSON التالية. **يجب أن يكون `total_score` هو مجموع الدرجات من 10.**

{
  "total_score": 0,
  "evaluation": [
    {
      "rule": "التعريف بالمنحة",
      "score": 0,
      "comment": "تعليقك ولماذا أخذ هذه الدرجة"
    },
    {
      "rule": "سؤال عن الاسم",
      "score": 0,
      "comment": "تعليقك"
    },
    {
      "rule": "الترحيب بالاسم",
      "score": 0,
      "comment": "تعليقك"
    },
    {
      "rule": "استئذان للوقت (للمكالمات الصادرة)",
      "score": 0,
      "comment": "تعليقك"
    },
    {
      "rule": "تجنب العامية والممنوعات",
      "score": 0,
      "comment": "تعليقك"
    },
    {
      "rule": "عدم مقاطعة الطالب",
      "score": 0,
      "comment": "تعليقك"
    }
  ],
  "positive_points": "اذكر هنا أهم نقاط القوة في أداء الموظف.",
  "areas_for_improvement": "اذكر هنا أهم النقاط التي تحتاج إلى تحسين."
}
"""

model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-05-20")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """صفحة الواجهة الرئيسية"""
    return render_template('index.html')

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
        
        return json_response, 200

    except Exception as e:
        print(f"!!!!!!!! AN ERROR OCCURRED !!!!!!!!\n{e}\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return jsonify({"error": f"An internal error occurred during analysis: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

