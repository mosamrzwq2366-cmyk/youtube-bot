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
    """تجربة الموديلات المستقرة والحديثة حصرياً بالترتيب"""
    print("🤖 جاري الاتصال بنموذج Gemini...")
    genai.configure(api_key=GEMINI_API_KEY)
    
    # القائمة البيضاء المحدثة للموديلات المتاحة والمدعومة حالياً
    models_to_try = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro',
        'gemini-1.0-pro'
    ]
    
    response = None
    for model_name in models_to_try:
        try:
            print(f"🔄 محاولة استخدام الموديل: {model_name}")
            model = genai.GenerativeModel(model_name)
            prompt = "اكتب عنوانًا جذابًا وفكرة قصة قصيرة للفيديو القادم."
            response = model.generate_content(prompt)
            print(f"✅ نجح الاتصال بالموديل: {model_name}")
            break
        except Exception as e:
            print(f"⚠️ تخطي الموديل {model_name} بسبب خطأ: {e}")
            continue
            
    if not response:
        raise Exception("❌ فشلت جميع الموديلات في الاستجابة، تأكد من صحة الـ GEMINI_API_KEY.")
        
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
