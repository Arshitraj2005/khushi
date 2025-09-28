import gdown
import subprocess
import time
import os

# 🎬 Google Drive IDs (replace with your own)
video_drive_id = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"   # Video file
audio_drive_id = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"   # Audio file

# 📂 Local file names
video_file = "video.mp4"
audio_file = "audio.mp3"

# 🔑 YouTube Stream Key (replace with yours)
stream_key = "2c4f-5sy5-q7tx-cz4t-0c8r"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"


def download_file(drive_id, output_file):
    """Download file from Google Drive if not exists"""
    if os.path.exists(output_file):
        print(f"✅ {output_file} already exists, skipping download.")
        return
    print(f"📥 Downloading {output_file} from Google Drive...")
    try:
        gdown.download(id=drive_id, output=output_file, quiet=False)
        print(f"✅ {output_file} download complete.")
    except Exception as e:
        print(f"🚨 Download failed for {output_file}: {e}")
        time.sleep(5)
        exit(1)


def stream_loop():
    """Start infinite streaming loop"""
    while True:
        print("🎥 Starting smooth YouTube stream (1080p30, stable keyframes)...")
        try:
            subprocess.run([
                "ffmpeg",
                "-re",                          # stream in realtime
                "-stream_loop", "-1", "-i", video_file,   # loop video forever
                "-stream_loop", "-1", "-i", audio_file,   # loop audio forever
                "-map", "0:v:0",                # take video from first input
                "-map", "1:a:0",                # take audio from second input
                "-c:v", "libx264",              # encode video → stable
                "-preset", "veryfast",
                "-b:v", "2500k",                # bitrate 2.5 Mbps
                "-maxrate", "3000k",            # peak bitrate
                "-bufsize", "6000k",            # buffer size
                "-g", "60",                     # keyframe every 2s (30fps → gop=60)
                "-r", "30",                     # 30fps
                "-c:a", "aac", "-b:a", "128k",  # encode audio
                "-pix_fmt", "yuv420p",          # required for YouTube
                "-f", "flv", stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed. Retrying in 5 sec...")
            time.sleep(5)


if __name__ == "__main__":
    download_file(video_drive_id, video_file)
    download_file(audio_drive_id, audio_file)
    stream_loop()
