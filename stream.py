import gdown
import subprocess
import time
import os

# ==== Google Drive IDs ====
video_drive_id = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"
audio_drive_id = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"

# ==== Local files ====
video_file = "video.mp4"
audio_file = "audio.mp3"

# ==== YouTube Stream Key ====
stream_key = "2c4f-5sy5-q7tx-cz4t-0c8r"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"


def download_file(drive_id, output_file):
    """Download file from Google Drive if not exists"""
    if os.path.exists(output_file):
        print(f"✅ {output_file} already exists, skipping download.")
        return
    print(f"📥 Downloading {output_file} ...")
    try:
        gdown.download(id=drive_id, output=output_file, quiet=False)
        print(f"✅ {output_file} download complete.")
    except Exception as e:
        print(f"🚨 Failed to download {output_file}: {e}")
        exit(1)


def stream_loop():
    """Run continuous YouTube Live stream"""
    while True:
        print("🚀 Starting YouTube Live Stream (1080p30, smooth loop)...")
        try:
            subprocess.run([
                "ffmpeg",
                "-stream_loop", "-1", "-i", video_file,   # loop video
                "-stream_loop", "-1", "-i", audio_file,   # loop audio
                "-map", "0:v:0", "-map", "1:a:0",         # video + audio mapping
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-b:v", "4500k",       # video bitrate
                "-maxrate", "5000k",
                "-bufsize", "10000k",
                "-g", "60", "-r", "30", 
                "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                "-f", "flv", stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed, retrying in 5 sec...")
            time.sleep(5)


if __name__ == "__main__":
    download_file(video_drive_id, video_file)
    download_file(audio_drive_id, audio_file)
    stream_loop()
