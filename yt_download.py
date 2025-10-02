from yt_dlp import YoutubeDL
from pathlib import Path

url = 'https://www.youtube.com/watch?v=VchuKL44s6E'
downloads_folder = f'{Path.home()}/Downloads'

ydl_opts = {
	"outtmpl": f'{downloads_folder}/%(title)s.%(ext)s',
	"format": 'bestvideo+bestaudio/best',
}

with YoutubeDL(ydl_opts) as ydl:
	ydl.download([url])
