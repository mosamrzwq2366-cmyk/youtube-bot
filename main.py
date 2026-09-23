import os
import requests
import json
import random
import time
import math
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# أبعاد ومواصفات فيديو الشورتس (9:16)
try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

def create_pro_stickman_video(output_path="auto_stickman.mp4"):
    """صناعة فيديو Stickman حركي مع مؤثرات نيون بصرياً بالكامل عبر الكود"""
    print("🎨 جاري إنشاء وتوليد فيديو Stickman حركي جديد...")
    
    if not HAS_CV2:
        raise Exception("مكتبة opencv غير مثبتة، أضف opencv-python-headless إلى requirements.txt")

    width, height = 720, 1280 # أبعاد Shorts
    fps = 30
    duration = 10 # 10 ثوانٍ أكشن مكثف
    total_frames = fps * duration

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    colors = [
        (0, 255, 255),  # نيون أصفر
        (255, 0, 255),  # نيون وردي
        (255, 255, 0),  # نيون أزرق
        (0, 255, 0)     # نيون أخضر
    ]
    stickman_color = random.choice(colors)

    for i in range(total_frames):
        # خلفية داكنة احترافية
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        t = i / fps
        center_x = int(width / 2 + math.sin(t * 3) * 150)
        center_y = int(height / 2 + math.cos(t * 5) * 80)
        
        # الرأس
        cv2.circle(frame, (center_x, center_y - 60), 30, stickman_color, 4)
        # الجسد
        cv2.line(frame, (center_x, center_y - 30), (center_x, center_y + 80), stickman_color, 6)
        
        # الأيدي (حركات قتالية سريعة)
        hand1_x = int(center_x + math.cos(t * 10) * 90)
        hand1_y = int(center_y + math.sin(t * 10) * 90)
        hand2_x = int(center_x - math.cos(t * 10) * 90)
        hand2_y = int(center_y - math.sin(t * 10) * 90)
        
        cv2.line(frame, (center_x, center_y - 10), (hand1_x, hand1_y), stickman_color, 5)
        cv2.line(frame, (center_x, center_y - 10), (hand2_x, hand2_y), stickman_color, 5)

        # الأقدام
        cv2.line(frame, (center_x, center_y + 80), (center_x - 40, center_y + 180), stickman_color, 5)
        cv2.line(frame, (center_x, center_y + 80), (center_x + 40, center_y + 180), stickman_color, 5)

        # مؤثرات النيون والإنفجارات البصرية خلف الشخصية
        if i % 10 < 5:
            cv2.circle(frame, (hand1_x, hand1_y), 15, (255, 255, 255), -1)
            cv2.circle(frame, (hand2_x, hand2_y), 15, (255, 255, 255), -1)

        out.write(frame)

    out.release()
    print("✅ تم إنشاء وتوليد ملف الفيديو أوتوماتيكياً بنجاح!")
    return output_path

def generate_viral_metadata():
    """توليد العنوان والوصف بـ Gemini"""
    print("🤖 جاري التواصل مع Gemini لتوليد العنوان والوصف...")
    models_to_try = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    
    unique_seed = int(time.time())
    prompt = f"""
    Create a highly viral, catchy YouTube Shorts title and description for a Stickman animation video.
    Title under 50 characters with strong Hook. Add hashtags like #shorts #stickman #animation #viral.
    Unique ID: {unique_seed}
    Format strictly as JSON with keys: "title", "description".
    """
    
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        try:
            res = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
            if res.status_code == 200:
                raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean_json)
                return parsed.get("title", f"Insane Stickman Action #{unique_seed}"), parsed.get("description", "#shorts #stickman")
        except:
            continue
            
    return f"Epic Stickman Battle #{unique_seed}", "Check out this insane stickman VFX action! #shorts #stickman #viral"

def upload_video_to_youtube(title, description, video_path):
    """الرفع التلقائي إلى يوتيوب"""
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
    
    body = {
        "snippet": {
            "title": title[:90],
            "description": description + "\n\n#shorts #stickman #animation #viral #trending",
            "tags": ["shorts", "stickman", "animation", "viral"],
            "categoryId": "1"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    print("📤 جاري رفع الفيديو المولّد إلى قناتك...")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"🎉 تم النشر بنجاح! رابط الفيديو: https://youtu.be/{response.get('id')}")

def main():
    print("🚀 بدء تشغيل البوت الأوتوماتيكي الذكي...")
    # 1. توليد وصناعة الفيديو من الصفر تلقائياً
    video_path = create_pro_stickman_video()
    
    # 2. كتابة العنوان والوصف الفيرل
    title, description = generate_viral_metadata()
    
    # 3. رفع الفيديو على يوتيوب
    upload_video_to_youtube(title, description, video_path)
    print("✨ انتهت المهمة بنجاح، البوت صنع ونشر الفيديو لوحده 100%!")

if __name__ == "__main__":
    main()
