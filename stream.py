import gdown
import subprocess
import time
import os

# Google Drive IDs
video_drive_id = "119IZhrca0P5d1-x-NQWHlcy5KBLtxpuV"  # 30s video
audio_drive_id = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"   # 1h30 audio

# Local file names
video_file = "video_30p.mp4"
audio_file = "audio.mp3"

# YouTube Stream Key
stream_key = "kmqx-xeh8-11ds-t258-a5sd"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

def download_file(drive_id, output_file):
    if os.path.exists(output_file):
        print(f"{output_file} exists, skipping download.")
        return
    print(f"Downloading {output_file}...")
    gdown.download(id=drive_id, output=output_file, quiet=False)

def stream_video_loop():
    """Loop video + audio both infinitely"""
    while True:
        print("Starting stream...")
        try:
            subprocess.run([
                "ffmpeg",
                "-re",                     
                "-stream_loop", "-1", "-i", video_file,   # loop video forever
                "-stream_loop", "-1", "-i", audio_file,   # loop audio forever
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", "copy",            
                "-c:a", "aac", "-b:a", "128k",
                "-f", "flv",
                stream_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("FFmpeg crashed, restarting in 5 sec...")
            time.sleep(5)

if __name__ == "__main__":
    download_file(video_drive_id, video_file)
    download_file(audio_drive_id, audio_file)
    stream_video_loop()
