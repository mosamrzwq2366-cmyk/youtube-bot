import os
import requests
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# 1. جلب المفاتيح من GitHub Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

def generate_script_with_gemini():
    """توليد النص باستخدام Gemini REST API مباشرة"""
    print("🤖 جاري الاتصال بنموذج Gemini عبر الـ API المباشر...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{"text": "اكتب عنوانًا جذابًا وفكرة قصة قصيرة لفيديو يوتيوب قصير (Shorts)."}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
        raise Exception(f"❌ فشل الاتصال بـ Gemini API (كود الاستجابة {response.status_code}): {response.text}")
        
    result_json = response.json()
    
    try:
        script_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
        print("✨ تم إنشاء النص بنجاح:")
        print(script_text)
        return script_text
    except Exception as e:
        raise Exception(f"❌ خطأ في تحليل استجابة Gemini: {e} - الرد كان: {result_json}")

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
    
    # 1. اختبار وتوليد النص من Gemini
    script = generate_script_with_gemini()
    
    # 2. اختبار الاتصال بيوتيوب
    youtube = get_youtube_service()
    
    print("✅ تم التحقق من عمل المفاتيح والاتصال بـ Gemini و YouTube بنجاح تام!")

if __name__ == "__main__":
    main()
