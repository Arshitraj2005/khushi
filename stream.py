import gdown
import subprocess
import time
import os

# 🎬 Google Drive IDs
video_drive_id = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"   # Video ID
audio_drive_id = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"   # Audio (music) ID

# 🎬 Local file names
video_file = "video.mp4"
audio_file = "music.mp3"

# 🔑 YouTube stream key
stream_key = "2c4f-5sy5-q7tx-cz4t-0c8r"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

def download_file(drive_id, local_file):
    if os.path.exists(local_file):
        print(f"✅ {local_file} already exists, skipping download.")
        return
    print(f"📥 Downloading {local_file} from Google Drive...")
    try:
        gdown.download(id=drive_id, output=local_file, quiet=False)
        print(f"✅ {local_file} download complete.")
    except Exception as e:
        print(f"🚨 Download failed for {local_file}: {e}")
        time.sleep(5)
        exit(1)

def stream_loop():
    while True:
        print("🎥 Starting stream with separate video + audio...")
        try:
            subprocess.run([
                "ffmpeg",
                "-stream_loop", "-1", "-re", "-i", video_file,  # Video loop
                "-stream_loop", "-1", "-re", "-i", audio_file,  # Audio loop
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",  # Stream will follow the shorter input if mismatch
                "-f", "flv",
                stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed. Retrying in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    download_file(video_drive_id, video_file)
    download_file(audio_drive_id, audio_file)
    stream_loop()
