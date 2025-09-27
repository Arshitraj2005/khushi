import gdown
import subprocess
import time
import os

# 🎬 Your Google Drive video ID
drive_id = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"
local_file = "video.mp4"

# 🔑 Your YouTube stream key (hardcoded as requested)
stream_key = "2c4f-5sy5-q7tx-cz4t-0c8r"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

def download_video():
    if os.path.exists(local_file):
        print("✅ Video already exists, skipping download.")
        return

    print("📥 Starting download from Google Drive...")
    try:
        gdown.download(id=drive_id, output=local_file, quiet=False)
        print("✅ Download complete.")
    except Exception as e:
        print(f"🚨 Download failed: {e}")
        time.sleep(5)
        exit(1)

def stream_loop():
    while True:
        print("🎥 Starting stream...")
        try:
            subprocess.run([
                "ffmpeg",
                "-re",
                "-i", local_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-f", "flv",
                stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed. Retrying in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    download_video()
    stream_loop()
