import yt_dlp
import subprocess
import time

# 🔗 Your YouTube Playlist URL
playlist_url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"

# 🔑 Your YouTube Stream Key (already pasted)
stream_key = "0akr-61bb-wc67-4qgr-c2xc"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

# 📦 Fetch all video URLs from playlist
def get_playlist_links(url):
    ydl_opts = {"extract_flat": True, "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return [entry['url'] for entry in info['entries'] if 'url' in entry]

# 🎥 Stream one video at a time
def stream_video(video_url):
    print(f"🎬 Streaming: {video_url}")
    try:
        subprocess.run([
            "ffmpeg", "-re", "-i", video_url,
            "-c:v", "copy", "-c:a", "aac",
            "-f", "flv", stream_url
        ], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ FFmpeg crashed. Skipping...")
        time.sleep(5)

# 🔁 Auto-Rotation Loop
def stream_playlist():
    while True:
        video_list = get_playlist_links(playlist_url)
        for video_url in video_list:
            stream_video(video_url)

# 🚀 Start Streaming
if __name__ == "__main__":
    stream_playlist()
