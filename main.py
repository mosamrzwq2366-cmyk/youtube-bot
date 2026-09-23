import os
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# 1. جلب المفاتيح من GitHub Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

def generate_script_with_gemini():
    """اختيار أحدث موديل أساسي متوفر وتوليد النص تلقائياً"""
    print("🤖 جاري الاتصال بنموذج Gemini...")
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("🔍 جاري فحص الموديلات المتاحة...")
    chosen_model_name = None
    
    # البحث عن موديل فلاش رئيسي ومناسب (استبعاد نماذج الصوت أو البريفيو الخاصة)
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            name = m.name.replace("models/", "")
            print(f" - متاح: {name}")
            # تفضيل موديلات الفلاش الحديثة مثل 3.6 أو 1.5
            if "flash" in name and "tts" not in name and "preview" not in name:
                chosen_model_name = name
                break
    
    # إذا لم يجد فلاش صافي، يأخذ أي موديل متاح يدعم التوليد
    if not chosen_model_name:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                chosen_model_name = m.name.replace("models/", "")
                break
                
    if not chosen_model_name:
        raise Exception("❌ لم يتم العثور على أي موديل متاح يدعم توليد المحتوى.")

    print(f"🚀 سيتم استخدام الموديل: {chosen_model_name}")
    
    model = genai.GenerativeModel(chosen_model_name)
    prompt = "اكتب عنوانًا جذابًا وفكرة قصة قصيرة للفيديو القادم."
    response = model.generate_content(prompt)
    
    print("✨ تم إنشاء النص بنجاح:")
    print(response.text)
    return response.text

def get_youtube_service():
    """إعداد وتأكيد الاتصال بـ YouTube Data API"""
    print("🔐 جاري الاتصال بحساب يوتيوب...")
    credentials = Credentials(
        token=None,
        refresh_token=YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YOUTUBE_CLIENT_ID,
        client_secret=YOUTUBE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube

def main():
    print("🚀 بدء تشغيل البوت التلقائي...")
    script = generate_script_with_gemini()
    youtube = get_youtube_service()
    print("✅ تم التحقق من عمل المفاتيح والاتصال بنجاح!")

if __name__ == "__main__":
    main()
