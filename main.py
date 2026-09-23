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
    """توليد نص الفيديو مع تجربة عدة موديلات تلقائياً"""
    print("🤖 جاري الاتصال بنموذج Gemini...")
    genai.configure(api_key=GEMINI_API_KEY)
    
    # قائمة الموديلات التي سيعمل البوت على تجربتها بالترتيب
    models_to_try = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro'
    ]
    
    response = None
    for model_name in models_to_try:
        try:
            print(f"🔄 محاولة استخدام الموديل: {model_name}")
            model = genai.GenerativeModel(model_name)
            prompt = "اكتب عنوانًا جذابًا وفكرة قصة قصيرة للفيديو القادم."
            response = model.generate_content(prompt)
            print(f"✅ تم النجاح باستخدام الموديل: {model_name}")
            break
        except Exception as e:
            print(f"⚠️ فشل الموديل {model_name} والسبب: {e}")
            continue
            
    if not response:
        raise Exception("عذراً، فشلت كل الموديلات في الاستجابة.")
        
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
    
    # 1. اختبار Gemini API
    script = generate_script_with_gemini()
    
    # 2. اختبار YouTube API
    youtube = get_youtube_service()
    
    print("✅ تم التحقق من عمل المفاتيح والاتصال بـ Gemini و YouTube بنجاح!")

if __name__ == "__main__":
    main()
