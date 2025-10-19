# دليل النشر السريع على Render 🚀

## ⚡ الخطوات السريعة

### 1️⃣ رفع على GitHub (لا تنفذ إلا بإذن)

```bash
# إنشاء Repository جديد على GitHub أولاً، ثم:
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2️⃣ نشر على Render (خدمة واحدة)

1. **New → Web Service**
2. **Connect Repository**
3. **الإعدادات:**
   ```
   Name: qa-calls
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```
4. **Environment Variables:**
   ```
   GEMINI_API_KEY = your_actual_api_key
   ```
5. **Create Web Service**

✅ **مبروك! مشروعك الآن Live على:**

- **رابط واحد للتطبيق الكامل:** `https://qa-calls.onrender.com`
- الواجهة والـ API على نفس الدومين (لا حاجة لتعديلات إضافية)

---

## 📝 ملاحظات مهمة

- ⚠️ **Free Plan**: الخدمة تدخل في وضع السكون بعد 15 دقيقة من عدم الاستخدام
- ⏱️ **أول طلب بعد السكون**: قد يستغرق 30-60 ثانية
- 🔐 **API Key**: لا تشاركه أو ترفعه على GitHub أبداً
- 🔄 **Auto Deploy**: أي تعديل تدفعه على GitHub سيُنشر تلقائياً

## 🐛 إذا ظهر أي خطأ

**تحقق من Logs:**

1. في Render Dashboard → اختر الخدمة
2. تبويب **Logs**
3. ابحث عن رسائل الخطأ

**الأخطاء الشائعة:**

- **Module not found**: تأكد من وجود المكتبة في `requirements.txt`
- **GEMINI_API_KEY not set**: تأكد من إضافة المتغير في Environment Variables
- **Port error**: Render يضبط المنفذ تلقائياً، لا تقلق

## 📊 مراقبة الـ Logs

في Render Dashboard:

1. اختر الخدمة (Backend أو Frontend)
2. تبويب **Logs**
3. راقب الأخطاء في الوقت الفعلي

## 💰 الترقية من Free Plan

للحصول على:

- عدم دخول في وضع السكون
- سرعة أعلى
- موارد أكثر

اختر **Paid Plan** من Render Dashboard.
