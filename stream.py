import gdown
import subprocess
import time
import os

# Google Drive IDs
video_drive_id = "1fWBOy78St8hSu_p9S29iyKqqVvSpts1X"  # 30p video, 1 min
audio_drive_id = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"   # 1h30 audio

# Local file names
video_file = "video_30p.mp4"
audio_file = "audio.mp3"

# YouTube Stream Key
stream_key = "2c4f-5sy5-q7tx-cz4t-0c8r"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

def download_file(drive_id, output_file):
    if os.path.exists(output_file):
        print(f"{output_file} exists, skipping download.")
        return
    print(f"Downloading {output_file}...")
    gdown.download(id=drive_id, output=output_file, quiet=False)

def stream_video_loop():
    """Loop video independently, then overlay audio in parts"""
    while True:
        print("Starting stream...")
        try:
            subprocess.run([
                "ffmpeg",
                "-re",                     # read video in real-time
                "-stream_loop", "-1", "-i", video_file,  # loop video forever
                "-i", audio_file,          # audio input (can be split)
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", "copy",            # CPU-friendly
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
