import gdown
import subprocess
import time
import os

drive_id = "1-iC97qVqueAT0kHL0sS93DBqZJpsP_ds"
local_file = "video.mp4"
stream_key = "0akr-61bb-wc67-4qgr-c2xc"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

def validate_video(path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=r_frame_rate,height", "-of", "default=noprint_wrappers=1", path],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.splitlines()
        resolution_ok = any("height=" in line and int(line.split("=")[1]) >= 480 for line in lines)
        fps_ok = any("r_frame_rate=" in line and eval(line.split("=")[1]) >= 24 for line in lines)

        audio_check = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
             "stream=codec_name", "-of", "default=noprint_wrappers=1", path],
            capture_output=True, text=True
        )
        has_audio = "codec_name=" in audio_check.stdout
        return resolution_ok and fps_ok, has_audio

    except Exception as e:
        print("❌ Video validation error:", e)
        return False, False

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
    valid, has_audio = validate_video(local_file)
    if not valid:
        print("⚠️ Video failed validation: check FPS/resolution")
        exit(1)

    while True:
        print("🎥 Starting stream...")
        cmd = ["ffmpeg", "-re", "-stream_loop", "-1", "-i", local_file]
        if not has_audio:
            cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        cmd += [
            "-c:v", "libx264", "-preset", "veryfast", "-r", "30", "-b:v", "2500k",
            "-c:a", "aac", "-b:a", "128k", "-f", "flv", stream_url
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("⚠️ FFmpeg crashed. Retrying in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    download_video()
    stream_loop()
