import os
import requests
import json
import time
import cv2
import numpy as np
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# الاستدعاء الشرطي لمكتبة MoviePy للدمج
try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
    HAS_MOVIEPY = True
except ImportError:
    HAS_MOVIEPY = False

# استدعاء المتغيرات البيئية من GitHub Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

def generate_60s_story_prompts():
    """1. توليد سيناريو دقيقة كاملة مقسم إلى 6 مشاهد بواسطة Gemini"""
    print("🧠 [1/4] Gemini API: جاري كتابة القصة والسيناريو...")
    
    unique_seed = int(time.time())
    prompt = f"""
    Create a funny 60-second viral 2D stickman cartoon scenario.
    Split the full story into exactly 6 distinct visual scenes (10 seconds each).
    
    Output strictly in valid JSON format with keys:
    "title": "Viral Short Title #shorts",
    "description": "Shorts description with hashtags",
    "scenes": [
        "Scene 1 visual description...",
        "Scene 2 visual description...",
        "Scene 3 visual description...",
        "Scene 4 visual description...",
        "Scene 5 visual description...",
        "Scene 6 visual description..."
    ]
    
    Seed: {unique_seed}
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        res = requests.post(url, headers=headers, data=json.dumps(data), timeout=20)
        raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"⚠️ خطأ Gemini: {e}")
        return {
            "title": f"Stickman vs Mosquito! #{unique_seed} #shorts #funny",
            "description": "Epic funny battle between stickman and mosquito! #shorts #animation",
            "scenes": [
                "2D stickman sitting peacefully at desk",
                "Annoying mosquito buzzing close to stickman ear",
                "Stickman gets angry and tries to slap mosquito",
                "Mosquito dodges and stickman hits his own face",
                "Stickman chases mosquito around room with swatter",
                "Stickman totally exhausted while mosquito rests on his nose"
            ]
        }

def render_single_scene(prompt_text, index, output_filename):
    """2. رسم وتوليد مشهد متحرك (10 ثوانٍ) باستخدام OpenCV"""
    print(f"🎨 [2/4] جاري رسم وتوليد المشهد رقم {index + 1}/6...")
    
    width, height = 720, 1280  # أبعاد Shorts
    fps = 30
    duration = 10
    total_frames = fps * duration

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    for i in range(total_frames):
        # خلفية رمادية فاتحة
        frame = np.full((height, width, 3), (230, 230, 230), dtype=np.uint8)
        t = i / fps
        center_x, center_y = 360, 640
        
        # حركة متغيرة بحسب المشهد
        offset = (index + 1) * 20
        mosq_x = int(center_x + np.sin(t * (10 + index)) * (150 + offset))
        mosq_y = int(center_y - 100 + np.cos(t * (12 + index)) * 80)

        # رسم شخصية Stickman
        cv2.circle(frame, (center_x, center_y - 80), 70, (0, 0, 0), 5) # الرأس
        cv2.circle(frame, (center_x - 25, center_y - 90), 20, (0, 0, 0), 3) # عين شمال
        cv2.circle(frame, (center_x + 25, center_y - 90), 20, (0, 0, 0), 3) # عين يمين
        cv2.circle(frame, (center_x - 25, center_y - 90), 6, (0, 0, 0), -1)
        cv2.circle(frame, (center_x + 25, center_y - 90), 6, (0, 0, 0), -1)
        
        # تعبيرات الفم
        if index % 2 == 0:
            cv2.ellipse(frame, (center_x, center_y - 50), (25, 15), 0, 0, 180, (0, 0, 0), 4)
        else:
            cv2.line(frame, (center_x - 20, center_y - 50), (center_x + 20, center_y - 50), (0, 0, 0), 4)

        # الجسد والأطراف
        cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 150), (0, 0, 0), 6)
        cv2.line(frame, (center_x, center_y + 30), (center_x - 80, center_y + 80), (0, 0, 0), 5)
        cv2.line(frame, (center_x, center_y + 30), (center_x + 80, center_y + 20), (0, 0, 0), 5)
        cv2.line(frame, (center_x, center_y + 150), (center_x - 50, center_y + 300), (0, 0, 0), 6)
        cv2.line(frame, (center_x, center_y + 150), (center_x + 50, center_y + 300), (0, 0, 0), 6)

        # الناموسة/الخصم
        cv2.circle(frame, (mosq_x, mosq_y), 9, (0, 0, 255), -1)

        out.write(frame)

    out.release()
    return output_filename

def combine_scenes_to_60s_video(scene_files, final_output="final_60s_video.mp4"):
    """3. تجميع الـ 6 مشاهد لتكوين فيديو 60 ثانية كاملاً"""
    print("🎬 [3/4] جاري دمج المقاطع في فيديو مدته 60 ثانية...")
    
    if HAS_MOVIEPY:
        clips = [VideoFileClip(f) for f in scene_files]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(final_output, fps=30, codec="libx264")
        for clip in clips:
            clip.close()
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(final_output, fourcc, 30, (720, 1280))
        for filename in scene_files:
            cap = cv2.VideoCapture(filename)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            cap.release()
        out.release()
        
    print("✅ تم إنتاج الفيديو النهائي بنجاح!")
    return final_output

def upload_to_youtube(title, description, video_path):
    """4. رفع الفيديو على يوتيوب عبر YouTube Data API"""
    print("📤 [4/4] YouTube API: جاري الرفع والنشر أوتوماتيكياً...")
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
            "description": description,
            "tags": ["shorts", "stickman", "animation", "funny", "meme"],
            "categoryId": "1"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"🎉 تم النشر بنجاح! الرابط: https://youtu.be/{response.get('id')}")

def main():
    print("🚀 بدء تشغيل دورة البوت المكتملة...")
    story_data = generate_60s_story_prompts()
    
    scene_files = []
    for idx, scene_prompt in enumerate(story_data["scenes"]):
        filename = f"scene_{idx}.mp4"
        render_single_scene(scene_prompt, idx, filename)
        scene_files.append(filename)
        
    final_video = combine_scenes_to_60s_video(scene_files)
    upload_to_youtube(story_data["title"], story_data["description"], final_video)
    
    # تنظيف الملفات المؤقتة
    for f in scene_files:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    main()
