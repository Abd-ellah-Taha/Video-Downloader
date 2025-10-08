import yt_dlp
import os
import uuid

def download_video(url, out_dir):
    uid = str(uuid.uuid4())[:8]
    # محدودات لتقليل المخاطر
    ydl_opts = {
        'outtmpl': os.path.join(out_dir, f'{uid}-%(title).50s.%(ext)s'),
        'noplaylist': False,
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        # يمكنك إضافة حدود حجم/وقت هنا إن احتجت
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    filename = ydl.prepare_filename(info)
    return {'title': info.get('title'), 'filename': os.path.basename(filename)}
