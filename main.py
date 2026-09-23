import os
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

def generate_script_with_gemini():
    print("🤖 جاري الاتصال بنموذج Gemini...")
    genai.configure(api_key=GEMINI_API_KEY)
    
    # طباعة قائمة المتاح تماماً لكي نرى نوع المفتاح
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"📌 موديل مدعوم بمفتاحك: {m.name}")
                model_name = m.name.replace("models/", "")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("اكتب عنواناً جذاباً لفيديو يوتيوب قصير.")
                print("✨ تم إنشاء النص بنجاح!")
                print(response.text)
                return response.text
    except Exception as e:
        print(f"⚠️ خطأ في الاتصال بالموديلات: {e}")
        
    raise Exception("❌ المفتاح المستخدم لا يدعم أي موديل generateContent. تأكد من إنشاء مفتاح من AI Studio.")

def get_youtube_service():
    print("🔐 جاري الاتصال بحساب يوتيوب...")
    credentials = Credentials(
        token=None,
        refresh_token=YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YOUTUBE_CLIENT_ID,
        client_secret=YOUTUBE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    return build("youtube", "v3", credentials=credentials)

def main():
    print("🚀 بدء تشغيل البوت التلقائي...")
    script = generate_script_with_gemini()
    youtube = get_youtube_service()
    print("✅ تم التحقق من عمل المفاتيح بنجاح!")

if __name__ == "__main__":
    main()
            
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
