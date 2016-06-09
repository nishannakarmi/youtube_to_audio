from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for
import youtube_dl
from utils import get_video_info

app = Flask(__name__)
# app.run(debug=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST', 'GET'])
def process_file():
    error = None
    if request.method == 'POST':
        print request.form.getlist('url')
        urls = request.form.getlist('url')
        if len(urls):
            for url in urls:
                info = get_video_info(url)
                if info and info['duration'] <= 360:
                    download_url = [url]
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'outtmpl': 'tmp/%(title)s-%(id)s.%(ext)s',
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(download_url)
                else:
                    print("LARGE VIDEO OR UNKNOW ERROR")

            return render_template('process_file.html')
        else:
            error = 'Invalid Url found'
            return redirect(url_for('home'))

    return redirect(url_for('home'))


@app.route('/download')
def download():
    return render_template('download.html')
