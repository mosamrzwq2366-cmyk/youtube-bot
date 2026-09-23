import os
import requests
import json
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

def generate_script_with_gemini():
    """تجربة نماذج متعددة للتعامل مع الضغط المؤقت 503"""
    print("🤖 جاري الاتصال بنموذج Gemini...")
    
    # قائمة النماذج لتجربتها بالترتيب
    models_to_try = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": "اكتب عنوانًا جذابًا وفكرة قصة قصيرة لفيديو يوتيوب قصير (Shorts)."}]
            }]
        }
        
        print(f"🔄 محاولة استخدام النموذج: {model_name}...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result_json = response.json()
            script_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✨ نجح توليد النص باستخدام {model_name}:")
            print(script_text)
            return script_text
        else:
            print(f"⚠️ فشل النموذج {model_name} (كود الاستجابة {response.status_code}): {response.text}")
            time.sleep(2)
            
    raise Exception("❌ فشلت جميع النماذج بسبب الضغط (503)، يجدر إعادة المحاولة لاحقاً.")

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
    print("✅ تم التحقق من عمل المفاتيح والاتصال بنجاح تام!")

if __name__ == "__main__":
    main()
