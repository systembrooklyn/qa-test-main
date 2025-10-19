# محلل المكالمات الذكي 🎙️

نظام تحليل مكالمات ذكي يستخدم Gemini AI لتقييم أداء الموظفين في مكالمات المنحة الدراسية.

## 🚀 المميزات

- تحليل تلقائي للمكالمات الصوتية (MP3, WAV)
- تقييم شامل من 10 درجات حسب معايير محددة
- واجهة عربية سهلة الاستخدام
- تقارير مفصلة مع نقاط القوة والتحسين

## 📋 المتطلبات

- Python 3.11+
- حساب Google AI (للحصول على Gemini API Key)
- حساب Render (للنشر)

## 🔧 التثبيت المحلي

### 1. تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### 2. إعداد المتغيرات البيئية

أنشئ ملف `.env` في جذر المشروع:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

احصل على API Key من: https://makersuite.google.com/app/apikey

### 3. تشغيل السيرفر

```bash
python app.py
```

السيرفر سيعمل على: `http://127.0.0.1:5000`

### 4. فتح الواجهة

افتح المتصفح واذهب إلى: `http://127.0.0.1:5000`

## 🌐 النشر على Render

### خطوة 1: رفع الكود على GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### خطوة 2: نشر على Render (Web Service واحد)

1. افتح [Render Dashboard](https://dashboard.render.com/)
2. اضغط **New → Web Service**
3. اربط repository الخاص بك
4. اختر الإعدادات التالية:
   - **Name**: `qa-calls`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. أضف Environment Variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: مفتاح Gemini API الخاص بك
6. اضغط **Create Web Service**

انتظر حتى ينتهي الـ deployment، وستحصل على رابط واحد للتطبيق بالكامل:
`https://qa-calls.onrender.com`

✅ **تم! التطبيق يعمل على رابط واحد يحوي الـ Frontend والـ Backend معاً**

## 📁 هيكل المشروع

```
qa-test-mainnnn/
├── app.py                 # Flask Backend API
├── templates/
│   └── index.html        # Frontend Interface
├── requirements.txt      # Python Dependencies
├── Procfile             # Render Deployment Config
├── runtime.txt          # Python Version
├── .env                 # Environment Variables (لا يُرفع على Git)
├── .env.example         # مثال للمتغيرات البيئية
├── .gitignore          # ملفات يتم تجاهلها في Git
├── DEPLOYMENT.md        # دليل النشر السريع
└── README.md           # هذا الملف
```

## 🔒 الأمان

- **لا ترفع** ملف `.env` على GitHub أبداً
- استخدم Environment Variables في Render لتخزين API Keys
- تأكد من أن `.gitignore` يحتوي على `.env`

## 🐛 استكشاف الأخطاء

### الخطأ: "لا يمكن الاتصال بسيرفر التحليل"

- تأكد من تشغيل السيرفر: `python app.py`
- افتح المتصفح على `http://127.0.0.1:5000` (وليس بفتح الملف مباشرة)
- في حالة CORS errors، تأكد من `flask-cors` مثبت بشكل صحيح

### الخطأ: "No GEMINI_API_KEY set"

- تأكد من وجود `.env` محلياً
- في Render، تأكد من إضافة المتغير في Environment Variables

### Backend على Render بطيء

- Render Free Plan يضع الخدمة في وضع السكون بعد 15 دقيقة من عدم الاستخدام
- أول طلب بعد السكون قد يستغرق 30-60 ثانية

## 📝 الترخيص

هذا المشروع للاستخدام الداخلي في "بروكلين بيزنس سكول".

## 👨‍💻 المطور

تم تطويره بواسطة: [اسمك هنا]

---

**ملاحظة**: هذا المشروع يستخدم Google Gemini AI. تأكد من الالتزام بـ [شروط استخدام Google AI](https://ai.google.dev/terms).
