import os
import requests
import json
import random
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# قراءة مفاتيح الأمان من بيئة العمل في جيت هب (GitHub Secrets)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

def generate_viral_metadata():
    """توليد عنوان، ووصف، وهوك أمريكي احترافي ومتجدد كلياً عبر Gemini"""
    print("🤖 جاري التواصل مع ذكاء Gemini لتوليد محتوى فيرل فريد...")
    
    models_to_try = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    
    themes = [
        "Epic parkour escape from high-speed laser traps and explosions",
        "Insane anime sword fight with glowing VFX and boss defeat",
        "Survival in a collapsing matrix digital world with super speed glitch",
        "Extreme martial arts combo and superhero powers against shadow monsters",
        "Zero-gravity space battle and gravity-defying stunts"
    ]
    chosen_theme = random.choice(themes)
    unique_seed = int(time.time() * 1000)
    
    prompt = f"""
    Create a highly viral, catchy YouTube Shorts title and description for a Stickman animation video.
    Core Theme for this clip: {chosen_theme} (Unique ID: {unique_seed}). Make it completely fresh and different.
    The title must be short, punchy (under 50 characters), and create an instant curiosity hook for US audiences.
    Add trending viral hashtags like #shorts #stickman #animation #epic #trending #vfx.
    
    Format the output strictly as JSON with keys: "title", "description".
    """
    
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    headers = {"Content-Type": "application/json"}
    
    raw_text = None
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=20)
            if response.status_code == 200:
                result_json = response.json()
                raw_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✨ نجح التوليد باستخدام النموذج: {model}")
                break
        except Exception as e:
            print(f"⚠️ فشل الاتصال مع {model}: {e}")
            continue
            
    if not raw_text:
        raise Exception("❌ فشل توليد المحتوى من جميع نماذج Gemini المتاحة.")
        
    try:
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean_json)
        title = parsed.get("title", f"Epic Stickman Action #{unique_seed}")
        description = parsed.get("description", "Insane Stickman VFX! #shorts #stickman")
        return title, description
    except:
        return f"Insane Stickman Challenge #{unique_seed}", raw_text[:200] + " #shorts #stickman #viral"

def get_random_video_file():
    """البحث عن ملفات فيديو داخل المستودع واختيار فيديو عشوائي للنشر"""
    print("📁 جاري البحث عن ملفات الفيديو المتاحة...")
    
    video_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".mp4") and file != "output.mp4":
                video_files.append(os.path.join(root, file))
                
    if not video_files:
        if os.path.exists("video.mp4"):
            return "video.mp4"
        raise Exception("❌ لم يتم العثور على أي ملف فيديو بصيغة mp4 في المستودع! يرجى رفع ملفات الفيديو الخاصة بك.")
        
    chosen_video = random.choice(video_files)
    print(f"🎬 تم اختيار الفيديو عشوائياً للنشر: {chosen_video}")
    return chosen_video

def upload_video_to_youtube(title, description, video_path):
    """رفع الفيديو على يوتيوب أوتوماتيكياً مع بيانات الـ SEO والهاشتاجات"""
    print("🔐 جاري المصادقة والاتصال ببوابة يوتيوب...")
    credentials = Credentials(
        token=None,
        refresh_token=YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YOUTUBE_CLIENT_ID,
        client_secret=YOUTUBE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": title[:90],
            "description": description + "\n\n#shorts #stickman #animation #epic #viral #trending #vfx",
            "tags": ["shorts", "stickman", "animation", "epic", "vfx", "viral", "trending", "action"],
            "categoryId": "1"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    print("📤 جاري رفع الفيديو الآن إلى منصة يوتيوب...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = request.execute()
    video_id = response.get('id')
    print(f"✅ تم نشر الفيديو بنجاح تام! رابط الفيديو: https://youtu.be/{video_id}")
    return video_id

def main():
    print("🚀 بدء تنفيذ نظام النشر الآلي بالكامل...")
    title, description = generate_viral_metadata()
    print(f"📌 العنوان المتولد: {title}")
    video_path = get_random_video_file()
    upload_video_to_youtube(title, description, video_path)
    print("🎉 تمت العملية بنجاح وبدون أي تدخل بشري!")

if __name__ == "__main__":
    main()
